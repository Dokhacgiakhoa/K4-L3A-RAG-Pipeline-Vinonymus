"""Offline checks for corpus scope, provenance and lossy HTML conversion."""

import hashlib
import json
from pathlib import Path
from datetime import datetime

from bs4 import BeautifulSoup

from src.task1_collect_legal_docs import DOCUMENT_SOURCES
from src.task2_crawl_news import ARTICLE_URLS, expand_tables

ROOT = Path(__file__).resolve().parents[1]


def test_merged_schedule_cells_keep_their_columns():
    soup = BeautifulSoup('<table><tr><td rowspan="2">Khóa V</td>'
                         '<td>Đợt 1</td><td rowspan="2">05/11/2026</td></tr>'
                         '<tr><td>Đợt 2</td></tr></table>', 'html.parser')
    expand_tables(soup)
    assert [[c.get_text() for c in row.select('td,th')] for row in soup.select('tr')] == [
        ['Khóa V', 'Đợt 1', '05/11/2026'], ['Khóa V', 'Đợt 2', '05/11/2026']]


def test_corpus_sources_are_reviewed_and_traceable():
    articles = sorted((ROOT / 'data/landing/news').glob('*.json'))
    assert len(articles) == len(ARTICLE_URLS)
    seen = set()
    for path in articles:
        item = json.loads(path.read_text(encoding='utf-8'))
        assert item['url'] in ARTICLE_URLS
        assert item['url'] not in seen
        seen.add(item['url'])
        assert datetime.fromisoformat(item['date_crawled']).tzinfo is not None
        body = item['content_markdown']
        assert 'thực chiến' in body.lower() or 'nhân tài ai' in body.lower(), \
            f"{path.name}: body does not mention the AI20K programme"
        # Facebook posts are from the official page; body may not always say 'vinuni'
        if 'facebook.com' not in item['url']:
            assert 'vinuni' in body.lower(), \
                f"{path.name}: non-Facebook article does not mention VinUni"
        assert len(body) >= 200
        assert item['content_sha256'] == hashlib.sha256(body.encode('utf-8')).hexdigest()
        assert not any(text in body for text in ['Device Detection Debug', 'Bài viết mới nhất', 'Có thể bạn thích', 'Ms. Phương Thảo'])
        md = (ROOT / 'data/standardized/news' / (path.stem + '.md')).read_text(encoding='utf-8')
        assert item['url'] in md and f'data/landing/news/{path.name}' in md
        assert body in md
    legal = {p.name for p in (ROOT / 'data/landing/legal').glob('*.pdf')}
    assert legal == {s['filename'] for s in DOCUMENT_SOURCES}


def test_faq_retains_questions_and_answers():
    item = json.loads((ROOT / 'data/landing/news/article_01.json').read_text(encoding='utf-8'))
    faq = item['content_markdown'].split('## Q&a', 1)[1]
    assert faq.count('?') >= 10
    assert 'không hỗ trợ chi phí đi lại và ăn ở' in faq
