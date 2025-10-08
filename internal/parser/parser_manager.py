import re
from typing import List, Dict, Any, Optional


class Parser:
    _re_percent = re.compile(
        r'(?<!\d)(\d{1,3})\s*%(\s*[-–—]\s*срочн\w+)?',
        re.IGNORECASE | re.UNICODE
    )
    _re_diag_block = re.compile(
        r'\[(.*?)\]',
        re.DOTALL | re.UNICODE
    )
    _re_questions_block = re.compile(
        r'\{(.*?)\}',
        re.DOTALL | re.UNICODE
    )
    _re_reco_after_keyword = re.compile(
        r'рекоменд\w*[:\-]?\s*(.+)$',
        re.IGNORECASE | re.UNICODE | re.DOTALL
    )

    def _clean(self, s: str) -> str:
        return re.sub(r'\s+', ' ', s).strip()

    def _parse_urgency(self, text: str) -> Optional[int]:
        m = self._re_percent.search(text)
        if not m:
            return None
        try:
            val = int(m.group(1))
            if 0 <= val <= 100:
                return val
        except ValueError:
            pass
        return None

    def _parse_diagnoses(self, text: str) -> List[Optional[str]]:
        m = self._re_diag_block.search(text)
        if not m:
            return [None, None, None]
        inside = m.group(1)
        parts = re.split(r'[,\n;/]+', inside)
        diags = []
        for p in parts:
            name = self._clean(p)
            if name:
                name = name.strip('\'"“”‘’`')
                if name:
                    diags.append(name)
        diags = diags[:3]
        while len(diags) < 3:
            diags.append(None)
        return diags

    def _parse_questions(self, text: str) -> Optional[List[str]]:
        m = self._re_questions_block.search(text)
        if not m:
            return None
        inside = m.group(1)
        parts = re.split(r'[,\n;]+', inside)
        qs = []
        for p in parts:
            q = self._clean(p)
            if q:
                q = re.sub(r'^\d+[\.\)]\s*', '', q)
                qs.append(q)
        return qs or None

    def _parse_recommendations(self, text: str) -> Optional[str]:
        questions_cut = self._re_questions_block.split(text)[0]
        m_kw = self._re_reco_after_keyword.search(questions_cut)
        if m_kw:
            rec = self._clean(m_kw.group(1))
            return rec or None
        m_diag = self._re_diag_block.search(questions_cut)
        if m_diag:
            tail = questions_cut[m_diag.end():]
            rec = self._clean(tail)
            if rec and not re.fullmatch(r'[\.\,\;\-\–—\s]*', rec):
                return rec
        return None

    def parse(self, data: str) -> Dict[str, Any]:
        """
        На вход подаётся любой текст, который 'врач' сгенерировал по вашему шаблону.
        На выходе — словарь:
        {
            "urgency": Optional[int],
            "diagnoses": List[Optional[str]] (ровно 3 элемента),
            "recommendations": Optional[str],
            "questions": Optional[List[str]]
        }
        Любые отсутствующие поля — None.
        """
        try:
            text = data if isinstance(data, str) else str(data)
            urgency = self._parse_urgency(text)
            diagnoses = self._parse_diagnoses(text)
            questions = self._parse_questions(text)
            recommendations = self._parse_recommendations(text)

            return {
                "urgency": urgency,
                "diagnoses": diagnoses,
                "recommendations": recommendations,
                "questions": questions
            }
        except Exception as e:
            return {
                "urgency": None,
                "diagnoses": [None, None, None],
                "recommendations": None,
                "questions": None,
                "error": str(e)
            }