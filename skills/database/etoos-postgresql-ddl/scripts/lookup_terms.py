#!/usr/bin/env python3
"""이투스 XML 용어사전에서 원문 후보를 조회하여 JSON 객체 하나로 출력한다.

논리명과 물리명은 자동 조합하거나 추천하지 않는다. 중복 항목을 포함해 원본
순서를 유지하며, source_index는 사전의 term 기준 1부터 시작하는 순번이다.
원문 속성의 빈 문자열은 보존하고, 원문에 없는 속성은 결과에도 넣지 않는다.
description 검색은 description과 physicalDescription을 함께 조회한다.
"""

import argparse
import json
from pathlib import Path
import sys
import unicodedata
import xml.etree.ElementTree as ET


SOURCE_FIELDS = ("name", "description", "physicalName", "physicalDescription", "tag")
SEARCH_FIELDS = {
    "logical": ("name",),
    "physical": ("physicalName",),
    "description": ("description", "physicalDescription"),
    "all": ("name", "description", "physicalName", "physicalDescription"),
}


class KoreanArgumentParser(argparse.ArgumentParser):
    """사용자 입력 오류를 한글 안내와 함께 표준 오류로 보낸다."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, f"오류: 명령행 옵션을 확인하세요. {message}\n")


def positive_integer(value):
    try:
        result = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("출력 제한은 1 이상의 정수여야 합니다.") from error
    if result < 1:
        raise argparse.ArgumentTypeError("출력 제한은 1 이상의 정수여야 합니다.")
    return result


def local_name(tag):
    """namespace 유무와 무관하게 XML 요소의 이름을 반환한다."""
    return tag.rsplit("}", 1)[-1]


def normalize(value):
    return unicodedata.normalize("NFC", value)


def main():
    parser = KoreanArgumentParser(
        description="이투스 용어사전의 논리명·물리명·설명을 검색합니다. 결과는 JSON입니다.",
        epilog="완전 일치가 기본입니다. 유사 후보 조회는 --match contains를 명시하세요.",
    )
    parser.add_argument("query", metavar="QUERY", help="조회할 검색어 한 개")
    parser.add_argument(
        "--field", choices=tuple(SEARCH_FIELDS), default="all",
        help="검색 대상: logical=논리명, physical=물리명, description=두 설명, all=전체 (기본: all)",
    )
    parser.add_argument(
        "--match", choices=("exact", "contains"), default="exact",
        help="검색 방식: exact=완전 일치, contains=부분 일치 (기본: exact)",
    )
    parser.add_argument(
        "--limit", type=positive_integer, default=20,
        help="출력할 최대 후보 수. 총 일치 수는 별도로 표시합니다 (기본: 20)",
    )
    parser.add_argument(
        "--dictionary", type=Path,
        default=Path(__file__).resolve().parent.parent / "references" / "etoos-terms.xdic",
        help="다른 용어사전 XML 파일 경로 (기본: 이 스킬의 references/etoos-terms.xdic)",
    )
    args = parser.parse_args()
    if not args.query.strip():
        parser.error("검색어는 빈 문자열이나 공백만으로 지정할 수 없습니다.")

    try:
        dictionary = args.dictionary.expanduser().resolve()
        root = ET.parse(dictionary).getroot()
    except (OSError, ET.ParseError, RuntimeError) as error:
        print(f"오류: 용어사전 파일을 읽거나 XML을 해석할 수 없습니다: {error}", file=sys.stderr)
        return 1
    if local_name(root.tag) != "TermDictionary":
        print("오류: XML 루트 요소가 TermDictionary가 아닙니다.", file=sys.stderr)
        return 1

    query = normalize(args.query)
    matched_count = 0
    matches = []
    terms = (element for element in root.iter() if local_name(element.tag) == "term")
    for source_index, term in enumerate(terms, start=1):
        values = (normalize(term.attrib[key]) for key in SEARCH_FIELDS[args.field] if key in term.attrib)
        matched = any(
            value == query if args.match == "exact" else query in value
            for value in values
        )
        if not matched:
            continue
        matched_count += 1
        if len(matches) < args.limit:
            matches.append({
                "source_index": source_index,
                **{key: term.attrib[key] for key in SOURCE_FIELDS if key in term.attrib},
            })

    result = {
        "dictionary": str(dictionary),
        "query": args.query,
        "field": args.field,
        "match": args.match,
        "matched_count": matched_count,
        "returned_count": len(matches),
        "truncated": matched_count > len(matches),
        "matches": matches,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
