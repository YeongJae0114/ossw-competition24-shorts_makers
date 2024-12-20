import requests
import os
import random
from dotenv import load_dotenv
from video_generator.keyword_extraction import extract_keywords
import time

load_dotenv()  # .env 파일에서 환경 변수 불러오기
API_KEY = os.getenv("PIXABAY_API_KEY")

# 카테고리와 해당 키워드 정의 (한국어)
categories_keywords = {
    # 'backgrounds': [
    #     '배경', '풍경', '전경', '장면', '스케치', '배경화면', '경관', '배경지식', '상황', '컨셉', 
    #     '비하인드', '환경', '기타', '화면', '기록', '디지털', '아트워크', '디자인', '조명', '색상', 
    #     '미적', '형태', '기후', '감각', '장식', '스토리', '주제', '특징', '풍부함', '화폭', 
    #     '배경음악', '애니메이션', '캐릭터', '환경설정', '비주얼', '대기', '장소', '이미지', '사물', '주변',
    #     '전통', '기억', '소리', '상징', '패턴', '추억', '미술', '미소', '비유', '개념'
    # ],
    'fashion': [
        '패션', '의류', '스타일', '트렌드', '모델', '디자인', '옷', '액세서리', '유행', '패션쇼', 
        '컬렉션', '패션아이콘', '디자이너', '뷰티', '옷차림', '소품', '색상', '스타일링', '룩북', '신발', 
        '코디', '주얼리', '헤어스타일', '세련됨', '패션 트렌드', '가방', '피팅', '데일리룩', '시즌', 
        '화장', '상표', '프레젠테이션', '마케팅', '행사', '네트워킹', '편안함', '원단', '재질', '소비',
        '브랜드', '이미지', '신상', '컬러', '패턴', '룩', '티셔츠', '바지', '정장', '패션 아이템'
    ],
    'nature': [
        '자연', '야생', '숲', '산', '바다', '강', '호수', '환경', '지구', '식물', 
        '동물', '기후', '생태계', '환경오염', '자원', '야생화', '지형', '식생', '고산', '평야', 
        '자연재해', '정글', '대양', '해변', '탐험', '생물다양성', '보호구역', '온실가스', '경관', 
        '위기', '자연현상', '기후변화', '보존', '경치', '산호초', '하천', '해양', '유전자', '서식지', 
        '특징', '탐험가', '식물학', '바이오', '산림', '습기', '사막', '식물성', '성장', '사상'
    ],
    # 'science': [
    #     '실험', '과학', '연구', '학습', '화학', '물리학', '생물학', '이론', '과학적', '데이터', 
    #     '과학기술', '현상', '가설', '논문', '실증', '변화', '분석', '관찰', '측정', '증명', 
    #     '실험실', '모델링', '기술', '혁신', '진화', '물질', '원자', '에너지', '생명체', 
    #     '조사', '결과', '복잡성', '시뮬레이션', '화합물', '상대성', '유전자', '생물', '가정', 
    #     '학문', '개념', '우주', '진화론', '화학반응', '입자', '고찰', '이론물리학', '화학물질', '현상학'
    # ],
    'education': [
        '학교', '학습', '교육', '교실', '학생', '선생님', '강의', '수업', '학위', '커리큘럼', 
        '교과서', '연구', '과정', '평가', '시험', '분석', '기술', '지식', '토론', '자기주도', 
        '학습방법', '목표', '계획', '발표', '참여', '멘토링', '조사', '온라인', '인증', 
        '전문성', '지적', '비판적', '토의', '숙제', '안내서', '자원', '토픽', '교수법', '대학', 
        '교육청', '리더십', '사회적', '조직', '전문교육', '학습환경', '발달', '코칭', '개발', '교수'
    ],
    'feelings': [
        '감정', '느낌', '사랑', '행복', '슬픔', '두려움', '기쁨', '정서', '우울', '희망', 
        '고민', '스트레스', '자존감', '안정감', '불안', '행운', '고통', '지지', '감사', 
        '편안함', '신뢰', '부정', '긍정', '상실', '감각', '고독', '지혜', '소통', 
        '용기', '결정', '자신감', '적응', '원망', '감정관리', '사고', '환희', '위안', 
        '자아', '경험', '선택', '상처', '친밀감', '기쁨', '안도감', '애정', '열정', '슬픔'
    ],
    'health': [
        '건강', '의학', '운동', '영양', '식이요법', '정신건강', '피트니스', '건강검진', '약물', '의사', 
        '병원', '치료', '예방', '면역', '재활', '약물치료', '상담', '증상', '식습관', '체중', 
        '비만', '건강식', '생활습관', '스트레스', '영양소', '건강관리', '질병', '질병예방', '심리', 
        '건강상식', '규칙', '자기관리', '상해', '안전', '대처', '생활습관병', '고혈압', '당뇨병', 
        '지식', '교육', '체험', '약사', '재정비', '면역력', '질병관리', '예방접종', '식이요법', '스트레스관리'
    ],
    'people': [
        '사람', '커뮤니티', '인간', '인물', '사회', '문화', '관계', '인종', '집단', '정치', 
        '이민', '역사', '성격', '소통', '감정', '생활', '행동', '규범', '유형', '아이덴티티', 
        '공동체', '리더', '지지', '참여', '갈등', '조화', '구성원', '문화적', '다양성', 
        '평등', '공감', '의사소통', '협력', '상호작용', '공동체의식', '가족', '세대', 
        '전통', '사회구조', '연대감', '자아정체성', '상징', '토론', '비판', '소외', '상호이해', '감정이입'
    ],
    'religion': [
        '종교', '신앙', '믿음', '교회', '기도', '신', '성경', '불교', '종교', '영성', 
        '예배', '의식', '신도', '철학', '신앙생활', '종교적 신념', '성전환', '명상', 
        '자아실현', '구원', '성스러운', '주말', '성직자', '종파', '기독교', '신화', 
        '신앙 공동체', '고백', '종교행사', '신성', '영혼', '영성추구', '유사종교', 
        '신비주의', '종교관', '사후세계', '신의 존재', '도덕', '종교적 삶', '종교문화', 
        '신앙의 기초', '성경해석', '종교적 경험', '종교적 의의', '공동체의식', '신의 뜻'
    ],
    'places': [
        '장소', '위치', '국가', '도시', '마을', '경치', '명소', '건물', '관광지', '여행지', 
        '유적지', '지역', '관광', '지리', '커뮤니티', '환경', '문화유산', '자연경관', 
        '여행', '명소', '휴양지', '산악지대', '해변', '대도시', '공원', '카페', '식당', 
        '시장', '이웃', '거리', '경관', '구역', '탐방', '명소', '목적지', '특징', 
        '활동', '축제', '체험', '관람', '주거지', '도시재생', '전통시장', '명물', 
        '주변', '숙소', '주거', '거리예술', '예술공간', '재미있는 장소', '체험장'
    ],
    'animals': [
        '동물', '야생', '포유류', '조류', '파충류', '양서류', '곤충', '해양동물', '애완동물', 
        '신체', '생물', '포식자', '생태계', '번식', '인간과의 관계', '행동', '대칭', 
        '진화', '서식', '환경', '관찰', '행동양식', '상호작용', '생리', '동물원', 
        '멸종', '각각', '개체', '해양동물', '조류', '포유류', '어류', '양서류', 
        '곤충', '온혈', '체온', '비행', '집단생활', '자연서식지', '사냥', '포식', 
        '종', '식사', '종 다양성', '생물학', '개체군', '행동학', '서식지', '환경보호', 
        '동물원 관리', '대체서식지', '보호', '생태계 복원', '애완동물 관리'
    ],
    'industry': [
        '산업', '제조', '생산', '공장', '경제', '노동', '기술', '인프라', '업종', '기업',
        '고용', '투자', '물류', '유통', '서비스', '경쟁', '마케팅', '판매', '수익', 
        '소비자', '시장', '혁신', '기획', '전략', '연구개발', '품질', '효율성', 
        '인력', '비즈니스모델', '고객', '기계', '자동화', '생산성', '시장성', 
        '해외시장', '공급망', '고부가가치', '기술개발', '산업혁신', '시장조사', '프랜차이즈', 
        '경영', '대량생산', '사업계획', '전문인력', '인재', '대응', '시장진입', '소비트렌드'
    ],
    'computer': [
        '컴퓨터', '기술', '소프트웨어', '하드웨어', '프로그래밍', '데이터베이스', 'AI', 
        'IT', '네트워크', '코딩', '시스템', '알고리즘', '운영체제', '클라우드', 
        '인터넷', '보안', '장비', '기기', '프로그램', '인공지능', '모바일', '웹', 
        '개발자', '프레임워크', '버전', 'API', '소스코드', '컴파일', '디버깅', 
        '프로토타입', '문서화', '설계', '기술적', '데이터', '기술혁신', '사이버', 
        '가상현실', '증강현실', '정보처리', '기술적 문제', '리포트', '분석', 
        '기술개발', '정보통신', '디지털화', '운영', '생산성', '어플리케이션'
    ],
    'food': [
        '음식', '요리', '식당', '식사', '레시피', '간식', '건강식', '디저트', '맛집', 
        '식문화', '조리법', '재료', '음료', '메뉴', '전통음식', '패스트푸드', '스낵', 
        '비건', '맛', '양식', '한식', '중식', '일식', '식사법', '요리책', '조리기구', 
        '조리법', '식사준비', '고기', '채소', '과일', '양념', '조리', '음식과학', 
        '특별식', '조화', '향신료', '식이요법', '고급요리', '그릴', '포장', '전문점', 
        '고급식당', '프레시푸드', '스무디', '전통음식', '이색요리', '다이어트식', '파티음식'
    ],
    'sports': [
        '스포츠', '경기', '대회', '팀', '운동', '선수', '훈련', '레크리에이션', 
        '종목', '챔피언', '피지컬', '전술', '리그', '경기장', '팬', '코치', 
        '올림픽', '세계선수권', '국제대회', '프로', '아마추어', '체육', 
        '체력', '기술', '경쟁', '체험', '자아도취', '시합', '스포츠맨십', 
        '기록', '상금', '대회준비', '결승', '순위', '상대', '전문가', 
        '체육관', '스포츠과학', '경기규칙', '트레이닝', '유니폼', '대회정보', 
        '스포츠의학', '심판', '체육수업', '문화', '소통', '모임', '팀워크'
    ],
    'transportation': [
        '교통', '차', '기차', '비행기', '버스', '교통수단', '도로', '항공', 
        '운송', '교통체계', '대중교통', '전철', '자전거', '차량', '셔틀', 
        '운전', '네비게이션', '안전', '서비스', '인프라', '터미널', 
        '포트', '정류장', '여행', '이동', '물류', '항로', '주차', 
        '도로교통', '교통법규', '시간표', '운전면허', '택시', 
        '교통혼잡', '교통신호', '교통비', '트럭', '국제교통', '수송', 
        '통행료', '대중교통비', '교통정책', '실시간교통', '효율성', 
        '이동수단', '차량관리', '운송업'
    ],
    'travel': [
        '여행', '여행지', '휴가', '관광', '탐험', '관광지', '여행사', '일정', 
        '경험', '여행준비', '숙소', '비행기', '차량', '일정표', '여행경비', 
        '여행자', '문화탐방', '기념품', '여행기', '안내서', '여행사진', 
        '전통', '음식', '레저', '관광코스', '가이드', '여행메이트', 
        '여행블로그', '교통편', '여행일정', '여행후기', '배낭여행', 
        '단체여행', '혼자여행', '일본', '유럽', '아시아', '탐험가', 
        '지도가', '여행용품', '여행계획', '여행지추천', '여행기념품', 
        '관광명소', '여행통신', '여행가이드'
    ],
    'buildings': [
        '건물', '건축', '건설', '디자인', '구조물', '주택', '아파트', '사무실', 
        '인프라', '시설', '설계', '개발', '토지', '구조', '기술', '환경', 
        '지속가능성', '재료', '공간', '도시', '공공건물', '상업시설', 
        '주거시설', '상징성', '모듈화', '문화재', '유지보수', '인테리어', 
        '신축', '리모델링', '효율성', '재개발', '시설물', '건축가', 
        '경관', '건축물', '설계도', '디자인', '디지털설계', '기술개발', 
        '건축기술', '구조엔지니어', '건축산업', '스마트시티', '고층건물', 
        '친환경건축', '시공', '대지조성', '건축자재', '기술적', '디지털화'
    ],
    'business': [
        '비즈니스', '재무', '회사', '기업', '상업', '거래', '마케팅', '회계', 
        '전략', '고객', '영업', '직원', '관리', '성과', '혁신', '투자', 
        '성과지표', '리더십', '경영전략', '사업계획', '경쟁', '위험관리', 
        '네트워킹', '산업트렌드', '분석', '프랜차이즈', '조직', '협력', 
        '성과분석', '비즈니스모델', '생산성', '고객서비스', '마케팅전략', 
        '브랜드', '대외활동', '소통', '고객만족', '제휴', '지속가능성', 
        '시장조사', '세일즈', '의사결정', '고객관계', '기업문화', 
        '위기관리', '기술개발', '소셜미디어'
    ],
    'music': [
        '음악', '노래', '악기', '멜로디', '리듬', '콘서트', '장르', '작곡', 
        '연주', '가사', '음악회', '밴드', '오케스트라', '사운드', 
        '악보', '음반', '라이브', '스트리밍', '음악가', '사운드트랙', 
        '음악프로듀서', '비트', '디제이', '작사', '해설', '리믹스', 
        '보컬', '트랙', '플롯', '장르혼합', '상징', '모티프', 
        '주제', '비교', '음악이론', '재즈', '클래식', '록', 
        '힙합', '대중음악', '모던', '전통음악', '조화', '선율', 
        '음악적 경험', '해설', '퍼포먼스', '뮤지션', '음악축제', 
        '정서', '공연', '사운드디자인'
    ]
}

def categorize_script(script):
    # 대본을 소문자로 변환 후 각 단어를 분리
    script_words = script.split()  # 한국어에서는 공백으로 단어 분리

    # 각 카테고리별로 카운트
    category_count = {category: 0 for category in categories_keywords}

    for word in script_words:
        for category, keywords in categories_keywords.items():
            if word in keywords:
                category_count[category] += 1

    # 가장 많은 키워드가 속한 카테고리를 반환
    best_category = max(category_count, key=category_count.get)

    return best_category

def pixabay(text):
    # 검색할 키워드와 요청 URL 설정 (비디오 검색)
    querys = extract_keywords(text)
    category = categorize_script(text)
    print(category)
    i = 1

    paths = []
    for query in querys:

        url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&lang=ko&category={category}'  # 언어 파라미터 추가
        # API 호출
        response = requests.get(url)
        data = response.json()

        if 'hits' in data and len(data['hits']) == 0:
            url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&lang=ko'
            response = requests.get(url)
            data = response.json()

        if not data['hits']:
            print(f"Pixabay에서 {query} 키워드에 대한 영상을 찾을 수 없습니다.")
            continue

        random_video = random.choice(data['hits'])  # 랜덤으로 하나 선택
        video_url = random_video['videos']['medium']['url']
        print(f"비디오 키워드: {query}")

        # 비디오 다운로드 및 크기 조정
        video_response = requests.get(video_url, stream=True)

        # 저장할 비디오 파일 경로
        video_filename = f'asset/video_{i}.mp4'
        with open(video_filename, 'wb') as f:
            f.write(video_response.content)
        print('비디오가 성공적으로 저장되었습니다.')
        i += 1
        paths.append(video_filename)
        time.sleep(1)  # 3초 대기

    return paths
