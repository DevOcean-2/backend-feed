"""
문자열 파싱 관련 유틸 함수
"""
import re
from typing import List


def extract_hashtags(content: str) -> List[str]:
    """
    해시태그 추출
    """
    hashtags = re.findall(r"#([\w가-힣]+)", content)  # '#' 다음에 오는 단어를 추출
    return hashtags
