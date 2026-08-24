from linkedin_pipeline import ai_card, palettes, queue_store


def _post(meta):
    return queue_store.Post(path=None, meta=meta, body="")


def test_explicit_palette_wins_over_topic():
    post = _post({"id": "1", "topic": "spring boot", "image": {"palette": "java"}})
    assert palettes.resolve_palette(post).name == "java"


def test_topic_match_java_and_spring():
    assert palettes.resolve_palette(_post({"id": "1", "topic": "Java records"})).name == "java"
    assert palettes.resolve_palette(_post({"id": "2", "topic": "Spring Security"})).name == "spring"


def test_javascript_topic_does_not_match_java():
    post = _post({"id": "1", "topic": "JavaScript async"})
    assert palettes.resolve_palette(post).name == "default"


def test_unknown_topic_falls_back_to_default():
    post = _post({"id": "1", "topic": "hybrid search"})
    assert palettes.resolve_palette(post).name == "default"


def test_ai_palette_is_orange():
    post = _post({"id": "1", "topic": "ai agents", "image": {"palette": "ai"}})
    pal = palettes.resolve_palette(post)
    assert pal.name == "ai" and pal.accent_name == "orange"


def test_orange_alias_resolves_to_ai_palette():
    post = _post({"id": "1", "topic": "whatever", "image": {"palette": "orange"}})
    assert palettes.resolve_palette(post).accent_name == "orange"


def test_ai_topic_autodetects_but_spring_ai_stays_green():
    assert palettes.resolve_palette(_post({"id": "1", "topic": "AI agents"})).name == "ai"
    assert palettes.resolve_palette(_post({"id": "2", "topic": "LLM eval"})).name == "ai"
    # "spring ai" must resolve to spring, not ai (spring pattern is checked first)
    assert palettes.resolve_palette(_post({"id": "3", "topic": "spring ai"})).name == "spring"


def test_unknown_explicit_palette_falls_back_to_default():
    post = _post({"id": "1", "topic": "java", "image": {"palette": "chartreuse"}})
    # invalid name is ignored, but topic still matches java
    assert palettes.resolve_palette(post).name == "java"


def test_build_prompt_free_injects_palette_hex():
    bullets = ["takeaway one", "takeaway two", "takeaway three"]
    java_post = _post({"id": "1", "topic": "java", "image": {
        "headline": "Records in Java", "bullets": bullets}})
    prompt = ai_card.build_prompt(java_post)
    assert "#e11d48" in prompt and "crimson/red" in prompt
    assert "#7c5cff" not in prompt  # the default violet must be gone

    default_post = _post({"id": "2", "topic": "hybrid search", "image": {
        "headline": "Hybrid search", "bullets": bullets}})
    assert "#7c5cff" in ai_card.build_prompt(default_post)
