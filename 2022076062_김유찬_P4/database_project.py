import sys
import pymysql as pym
import time
from datetime import datetime

# connect
db = pym.connect(
    host="localhost",       
    user="root",           
    password="abcd",       
    charset="utf8mb4"       
)

cursor = db.cursor()
cursor.execute('USE music_stream_service')

def main_menu():
    while True:
        print("메뉴를 선택하세요: ")
        print("1. admin 전용")
        print("2. user 전용")
        print("3. admin 회원가입")
        print("0. exit")

        sel = int(input("입력:"))
        if sel == 0:
            db.close()
            print("종료됐습니다.")
            time.sleep(1)
            break
        elif sel == 1:
            adminMode()
        elif sel == 2:
            userMode()
        elif sel == 3:
            adminSignUp()
        else:
            print("잘못된 입력입니다")
            time.sleep(1)

def adminMode():
    while True:
        adminNumber = int(input("관리자 번호를 입력하세요: "))
        cursor.execute("SELECT 닉네임 FROM 관리자 WHERE ANumber = %s", (adminNumber,))
        result = cursor.fetchone()
        if result:
            nickname = result[0] 
            print("\n환영합니다, " + nickname + "님!\n")
            time.sleep(1)
            break 
        else:
            print("유효하지 않은 관리자 번호입니다. 다시 시도하세요.\n")
            time.sleep(1)
            return
    while True:
        print("-----관리자 전용 메뉴-----")
        print("관리자 : " + nickname)
        print("1. 사용자 추가")
        print("2. 사용자 삭제")
        print("3. 음악 추가")
        print("4. 음악 삭제")
        print("5. 탈퇴하기")
        print("0. 이전 메뉴로 돌아가기\n")

        sel = int(input("입력 : "))
        if sel == 1:
            addUser(adminNumber)
        elif sel == 2:
            deleteUser(adminNumber)
        elif sel == 3:
            addMusic(adminNumber)
        elif sel == 4:
            deleteMusic(adminNumber)
        elif sel == 5:
            deleteAdmin(adminNumber)
        elif sel == 0:
            break
        else:
            print("잘못된 입력입니다")
            time.sleep(1)

def addUser(adminNumber):
    print("사용자 추가를 시작합니다.\n")
    time.sleep(1)
    
    u_number = int(input("사용자 번호 : "))

    # 중복 확인
    cursor.execute("SELECT COUNT(*) FROM 사용자 WHERE UNumber = %s", (u_number,))
    count = cursor.fetchone()[0]
    if count > 0:
        print("\n중복된 사용자 번호입니다. 다른 번호를 입력하세요.\n")
        time.sleep(1)
        return
    
    name = input("이름 : ")
    gender = input("성별 (M/F) : ").upper()
    phone_number = input("전화번호 (예: 010-1234-5678) : ")
    nickname = input("닉네임 : ")
    address = input("집주소 : ")
    birth_date = input("생년월일 (YYYY-MM-DD) : ")
    email = input("메일주소 : ")
    time.sleep(1)

    # 입력값 확인
    print("\n입력한 정보:")
    print(f"사용자 번호: {u_number}")
    print(f"이름: {name}")
    print(f"성별: {gender}")
    print(f"전화번호: {phone_number}")
    print(f"닉네임: {nickname}")
    print(f"집주소: {address}")
    print(f"생년월일: {birth_date}")
    print(f"메일주소: {email}")
    print(f"관리자 번호: {adminNumber}")

    confirm = input("위 정보를 저장하시겠습니까? (Y/N): ").upper()

    if confirm == "Y":
        # 데이터베이스에 INSERT
        cursor.execute("""
            INSERT INTO 사용자 (UNumber, 이름, 성별, 전화번호, 닉네임, 집주소, 생년월일, 메일주소, ANo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (u_number, name, gender, phone_number, nickname, address, birth_date, email, adminNumber))
        db.commit()  # 변경 사항 저장
        print("\n새로운 사용자가 성공적으로 추가되었습니다.\n")
        time.sleep(1)
    else:
        print("\n사용자 추가가 취소되었습니다.\n")
        time.sleep(1)

def deleteUser(adminNumber):
    print("사용자 삭제를 시작합니다.\n")
    time.sleep(1)
    u_number = int(input("삭제할 사용자 번호 : "))

    # 사용자 확인
    cursor.execute("SELECT 이름, 닉네임, ANo FROM 사용자 WHERE UNumber = %s", (u_number,))
    result = cursor.fetchone()

    if result:
        name, nickname, user_admin_number = result
        if user_admin_number != adminNumber:
            print("\n권한이 없습니다. 이 사용자는 다른 관리자가 소유하고 있습니다.\n")
            time.sleep(1)
            return
        
        print(f"삭제할 사용자: {name} (닉네임: {nickname})")

        # 삭제 사유 입력
        reason = input("삭제 사유를 입력하세요: ")

        confirm = input("정말 삭제하시겠습니까? (Y/N): ").upper()
        if confirm == "Y":
            # 사용자 삭제
            cursor.execute("DELETE FROM 사용자 WHERE UNumber = %s", (u_number,))
            db.commit()  # 변경 사항 저장
            print(f"\n사용자 삭제가 완료되었습니다.\n삭제 사유 : {reason}\n")
            time.sleep(1)
        else:
            print("\n사용자 삭제가 취소되었습니다.\n")
            time.sleep(1)
    else:
        print("\n해당 사용자 번호가 존재하지 않습니다.\n")
        time.sleep(1)


def addMusic(adminNumber):
    print("음악 추가를 시작합니다.\n")
    time.sleep(1)
    
    m_number = int(input("음악 번호 (MNumber) : "))

    # 중복 확인
    cursor.execute("SELECT COUNT(*) FROM 음악 WHERE MNumber = %s", (m_number,))
    count = cursor.fetchone()[0]
    if count > 0:
        print("\n중복된 음악 번호입니다. 다른 번호를 입력하세요.\n")
        time.sleep(1)
        return

    # 음악 정보 입력받기
    singer_name = input("가수 이름 : ")
    singer_gender = input("가수 성별 (M/F) : ").upper()
    title = input("제목 : ")
    genres = [genre.strip() for genre in input("장르 (쉼표로 구분하여 입력, 예: K-Pop,댄스): ").split(",")]

    # 피처링 데이터 입력
    featuring = input("피처링 여부 (Y/N): ").strip().upper()
    featuring_name = None
    featuring_gender = None
    if featuring == "Y":
        featuring_name = input("피처링 아티스트 이름 : ").strip()
        featuring_gender = input("피처링 아티스트 성별 (M/F): ").upper()

    # 입력값 확인
    print("\n입력한 정보:")
    print(f"음악 번호 : {m_number}")
    print(f"가수 이름 : {singer_name}")
    print(f"가수 성별 : {singer_gender}")
    print(f"제목 : {title}")
    print(f"장르 : {', '.join(genres)}")
    if featuring == "Y":
        print(f"피처링 아티스트 : {featuring_name} ({featuring_gender})")
    else:
        print("피처링 여부 : N")
    print(f"관리자 번호 : {adminNumber}")

    confirm = input("위 정보를 저장하시겠습니까? (Y/N) : ").upper()

    if confirm == "Y":
        # 음악 테이블에 INSERT
        cursor.execute("""
            INSERT INTO 음악 (MNumber, 가수이름, 가수성별, 제목, ANum)
            VALUES (%s, %s, %s, %s, %s)
        """, (m_number, singer_name, singer_gender, title, adminNumber))
        
        # 피처링 테이블에 INSERT (있을 경우에만)
        if featuring == "Y" and featuring_name and featuring_gender:
            cursor.execute("""
                INSERT INTO 피처링 (이름, 성별, MNo)
                VALUES (%s, %s, %s)
            """, (featuring_name, featuring_gender, m_number))

        # 음악장르 테이블에 INSERT (여러 장르 처리)
        for genre in genres:
            genre = genre.strip()  # 앞뒤 공백 제거
            cursor.execute("""
                INSERT INTO 장르 (음악장르, MNumber)
                VALUES (%s, %s)
            """, (genre, m_number))

        db.commit()  # 변경 사항 저장
        print("\n새로운 음악이 성공적으로 추가되었습니다.\n")
        time.sleep(1)
    else:
        print("\n음악 추가가 취소되었습니다.\n")
        time.sleep(1)


def deleteMusic(adminNumber):
    print("음악 삭제를 시작합니다.\n")
    time.sleep(1)

    # 삭제할 음악 번호 입력
    m_number = int(input("삭제할 음악 번호 (MNumber): "))

    # 음악 확인
    cursor.execute("SELECT 제목, 가수이름, ANum FROM 음악 WHERE MNumber = %s", (m_number,))
    result = cursor.fetchone()

    if result:
        title, singer_name, music_admin_number = result

        if music_admin_number != adminNumber:
            print("\n권한이 없습니다. 이 음악은 다른 관리자가 소유하고 있습니다.\n")
            time.sleep(1)
            return
        
        print(f"삭제할 음악: '{title}' by {singer_name}")

        # 삭제 확인
        confirm = input("정말 삭제하시겠습니까? (Y/N): ").upper()
        if confirm == "Y":
            # 음악 삭제
            cursor.execute("DELETE FROM 음악 WHERE MNumber = %s", (m_number,))
            db.commit() 
            print(f"\n음악 '{title}' by {singer_name}이(가) 성공적으로 삭제되었습니다.\n")
        else:
            print("\n음악 삭제가 취소되었습니다.\n")
            time.sleep(1)
    else:
        print("\n해당 음악 번호가 존재하지 않습니다.\n")
        time.sleep(1)

def deleteAdmin(adminNumber):
    print("관리자 탈퇴를 시작합니다.\n")
    time.sleep(1)

    # 관리자가 관리하는 음악 확인
    cursor.execute("SELECT COUNT(*) FROM 음악 WHERE ANum = %s", (adminNumber,))
    music_count = cursor.fetchone()[0]

    # 관리자가 관리하는 사용자 확인
    cursor.execute("SELECT COUNT(*) FROM 사용자 WHERE ANo = %s", (adminNumber,))
    user_count = cursor.fetchone()[0]

    if music_count > 0 or user_count > 0:
        print("관리자가 관리하고 있는 음악 또는 사용자가 있어서 탈퇴할 수 없습니다.\n")
        if music_count > 0:
            print(f"관리 중인 음악 수: {music_count}")
        if user_count > 0:
            print(f"관리 중인 사용자 수: {user_count}")
        print('')
        time.sleep(1)
        return

    # 탈퇴 가능 여부 확인
    confirm = input("관리 중인 음악이나 사용자가 없습니다. 정말 탈퇴하시겠습니까? (Y/N): ").upper()
    if confirm == "Y":
        cursor.execute("DELETE FROM 관리자 WHERE ANumber = %s", (adminNumber,))
        db.commit()
        print("\n관리자 탈퇴가 성공적으로 완료되었습니다.")
        print("프로그램을 종료합니다.")
        time.sleep(1)
        sys.exit()
    else:
        print("\n관리자 탈퇴가 취소되었습니다.\n")
        time.sleep(1)

def userMode():
    while True:
        userNumber = int(input("사용자 번호를 입력하세요: "))
        cursor.execute("SELECT 닉네임 FROM 사용자 WHERE UNumber = %s", (userNumber,))
        result = cursor.fetchone()
        if result:
            nickname = result[0]
            print(f"\n환영합니다, {nickname}님!\n")
            time.sleep(1)
            break
        else:
            print("유효하지 않은 사용자 번호입니다. 다시 시도하세요.\n")
            time.sleep(1)
            return
    
    while True:
        cursor.execute("SELECT COUNT(*) FROM 프리미엄 WHERE UNo = %s", (userNumber,))
        premium_status = cursor.fetchone()[0]
        print("-----사용자 전용 메뉴-----")
        if premium_status > 0:
            print(f"사용자 : {nickname} (Premium)")
        else:
            print(f"사용자 : {nickname}")
        print("1. 음악 검색")
        print("2. 플레이 리스트")
        print("3. 프리미엄 등록/해제")
        print("0. 이전 메뉴로 돌아가기\n")
    
        sel = int(input("입력 : "))
        if sel == 1:
            searchMusic(userNumber)
        elif sel == 2:
            Playlist(userNumber)
        elif sel == 3:
            Premium(userNumber)
        elif sel == 0:
            break
        else:
            print("잘못된 입력입니다.\n")
            time.sleep(1)

def searchMusic(userNumber):
    while True:
        cursor.execute("SELECT 닉네임 FROM 사용자 WHERE UNumber = %s", (userNumber,))
        result = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM 프리미엄 WHERE UNo = %s", (userNumber,))
        premium_status = cursor.fetchone()[0]
        print("\n-----음악 검색 메뉴-----")
        nickname = result[0]
        if premium_status > 0:
            print(f"사용자 : {nickname} (Premium)")
        else:
            print(f"사용자 : {nickname}")
        print("1. 인기 Top5")
        print("2. 제목으로 검색하기")
        print("3. 가수로 검색하기")
        print("4. 장르로 검색하기")
        print("0. 이전 메뉴로 돌아가기\n")

        sel = int(input("입력: "))
        
        if sel == 0:
            return
        elif sel == 1:
            top5Music(userNumber)
        elif sel == 2:
            searchByTitle(userNumber)
        elif sel == 3:
            searchBySinger(userNumber)
        elif sel == 4:
            searchByGenre(userNumber)
        else:
            print("\n잘못된 입력입니다. 다시 시도하세요.\n")
            time.sleep(1)

def top5Music(userNumber):
    print("\n-----인기 Top 5-----")

    # 좋아요 수 기준으로 상위 5개 음악과 피처링 정보 가져오기
    cursor.execute("""
        SELECT 
            음악.MNumber, 
            음악.제목, 
            음악.가수이름, 
            GROUP_CONCAT(피처링.이름 SEPARATOR ', ') AS 피처링정보
        FROM 음악
        LEFT JOIN 피처링 ON 음악.MNumber = 피처링.MNo
        GROUP BY 음악.MNumber, 음악.제목, 음악.가수이름
        ORDER BY 음악.좋아요수 DESC
        LIMIT 5
    """)
    top_music = cursor.fetchall()

    # 결과 출력
    for idx, (m_number, title, singer_name, featuring) in enumerate(top_music, start=1):
        featuring_text = f" (feat. {featuring})" if featuring else ""
        print(f"{idx}. {title} - {singer_name}{featuring_text}")
    
    print("0. 이전 메뉴로 돌아가기\n")
    
    # 사용자 입력
    selected = int(input("노래 선택: "))
    if selected == 0:
        return
    elif selected < 1 or selected > len(top_music):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 선택한 노래의 MNumber 가져오기
    selected_music = top_music[selected - 1][0]
    
    # Music 함수 호출
    Music(userNumber, selected_music)


def searchByTitle(userNumber):
    title = input("\n제목을 입력하세요: ").strip()
    
    if not title:
        print("\n입력된 제목이 없습니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 제목과 피처링 정보를 포함한 노래 검색
    cursor.execute("""
        SELECT 
            음악.MNumber, 
            음악.제목, 
            음악.가수이름, 
            GROUP_CONCAT(피처링.이름 SEPARATOR ', ') AS 피처링정보
        FROM 음악
        LEFT JOIN 피처링 ON 음악.MNumber = 피처링.MNo
        WHERE 음악.제목 LIKE %s
        GROUP BY 음악.MNumber, 음악.제목, 음악.가수이름
        LIMIT 5
    """, ('%' + title + '%',))  # 제목에 부분 일치 검색 (LIKE 사용)
    results = cursor.fetchall()

    if not results:
        print("\n일치하는 항목이 없습니다.\n")
        time.sleep(1)
        return

    # 결과 출력
    print("\n-----검색 결과-----")
    for idx, (m_number, title, singer_name, featuring) in enumerate(results, start=1):
        featuring_text = f" (feat. {featuring})" if featuring else ""
        print(f"{idx}. {title} - {singer_name}{featuring_text}")

    print("0. 이전 메뉴로 돌아가기\n")

    # 선택
    selected = int(input("노래 번호를 선택하세요: "))
    
    if selected == 0:
        return
    elif selected < 1 or selected > len(results):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 선택한 노래 정보 가져오기
    selected_music = results[selected - 1][0]
    Music(userNumber, selected_music)


def searchBySinger(userNumber):
    # 가수 이름 입력받기
    singer_name = input("\n가수 이름을 입력하세요: ").strip()

    if not singer_name:
        print("\n입력된 가수 이름이 없습니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 메인 가수 및 피처링 가수로 참여한 노래 검색 (JOIN 연산으로 통합)
    cursor.execute("""
        SELECT 음악.MNumber, 음악.제목, 음악.가수이름, GROUP_CONCAT(피처링.이름 SEPARATOR ', ') AS featuring_artists
        FROM 음악
        LEFT JOIN 피처링 ON 음악.MNumber = 피처링.MNo
        WHERE 음악.가수이름 LIKE %s OR 피처링.이름 LIKE %s
        GROUP BY 음악.MNumber, 음악.제목, 음악.가수이름
        LIMIT 5
    """, ('%' + singer_name + '%', '%' + singer_name + '%'))
    songs = cursor.fetchall()

    # 결과 출력
    if not songs:
        print("\n일치하는 항목이 없습니다.\n")
        time.sleep(1)
        return

    print("\n-----검색 결과-----")
    for idx, (m_number, title, singer, featuring) in enumerate(songs, start=1):
        featuring_text = f" (feat. {featuring})" if featuring else ""
        print(f"{idx}. {title} - {singer}{featuring_text}")

    print("0. 이전 메뉴로 돌아가기\n")

    # 노래 선택
    selected = int(input("노래 번호를 선택하세요: "))
    
    if selected == 0:
        return

    if selected < 1 or selected > len(songs):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 선택한 노래의 MNumber를 가져오기
    selected_music = songs[selected - 1][0]
    Music(userNumber, selected_music)

def searchByGenre(userNumber):
    # 장르 이름 입력받기
    genre_name = input("\n장르를 입력하세요: ").strip()

    if not genre_name:
        print("\n입력된 장르가 없습니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 장르에 해당하는 음악과 피처링 정보 검색
    cursor.execute("""
        SELECT 
            음악.MNumber, 
            음악.제목, 
            음악.가수이름, 
            GROUP_CONCAT(피처링.이름 SEPARATOR ', ') AS 피처링정보
        FROM 음악
        JOIN 장르 ON 음악.MNumber = 장르.MNumber
        LEFT JOIN 피처링 ON 음악.MNumber = 피처링.MNo
        WHERE 장르.음악장르 LIKE %s
        GROUP BY 음악.MNumber, 음악.제목, 음악.가수이름
        LIMIT 5
    """, ('%' + genre_name + '%',))
    genre_songs = cursor.fetchall()

    # 결과 출력
    if not genre_songs:
        print("\n일치하는 항목이 없습니다.\n")
        time.sleep(1)
        return

    print("\n-----검색 결과-----")

    # 검색된 노래 출력
    for idx, (m_number, title, singer, featuring) in enumerate(genre_songs, start=1):
        featuring_text = f" (feat. {featuring})" if featuring else ""
        print(f"{idx}. {title} - {singer}{featuring_text}")

    print("0. 이전 메뉴로 돌아가기\n")

    # 노래 선택
    selected = int(input("노래 번호를 선택하세요: "))

    if selected == 0:
        return

    if selected < 1 or selected > len(genre_songs):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 선택한 노래의 MNumber를 가져오기
    selected_music = genre_songs[selected - 1][0]
    Music(userNumber, selected_music)

def Playlist(userNumber):
    while True:
        cursor.execute("SELECT 닉네임 FROM 사용자 WHERE UNumber = %s", (userNumber,))
        result = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM 프리미엄 WHERE UNo = %s", (userNumber,))
        premium_status = cursor.fetchone()[0]
        print("\n-----플레이 리스트 메뉴-----")
        nickname = result[0]
        if premium_status > 0:
            print(f"사용자 : {nickname} (Premium)")
        else:
            print(f"사용자 : {nickname}")
        print("1. 내 플레이 리스트")
        print("2. 플레이 리스트 생성")
        print("3. 플레이 리스트 삭제")
        print("4. 플레이 리스트 내 음악 삭제")
        print("5. 플레이 리스트 검색하기")
        print("0. 이전 메뉴로 돌아가기\n")

        sel = int(input("입력 : "))
        if sel == 1:
            myPlaylist(userNumber)
        elif sel == 2:
            createPlaylist(userNumber)
        elif sel == 3:
            deletePlaylist(userNumber)
        elif sel == 4:
            deleteMusicInPlaylist(userNumber)
        elif sel == 5:
            findPlaylist(userNumber)
        elif sel == 0:
            break
        else:
            print("잘못된 입력입니다.\n")
            time.sleep(1)

def myPlaylist(userNumber):
    # 사용자 플레이리스트 조회
    cursor.execute("""
        SELECT DISTINCT 이름
        FROM 플레이리스트
        WHERE UNo = %s
    """, (userNumber,))
    playlists = cursor.fetchall()

    if not playlists:
        print("\n내 플레이리스트가 없습니다.\n")
        time.sleep(1)
        return
    
    cursor.execute("SELECT 닉네임 FROM 사용자 WHERE UNumber = %s", (userNumber,))
    result = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM 프리미엄 WHERE UNo = %s", (userNumber,))
    premium_status = cursor.fetchone()[0]
    nickname = result[0]
    if premium_status > 0:
        print(f"\n사용자 : {nickname} (Premium) 플레이 리스트")
    else:
        print(f"\n사용자 : {nickname} 플레이 리스트")
    for idx, (playlist_name,) in enumerate(playlists, start=1):
        print(f"{idx}. {playlist_name}")
    print("0. 이전 메뉴로 돌아가기\n")
    selected = int(input("플레이 리스트 번호를 선택하세요: "))

    if selected == 0:
        return
    elif selected < 1 or selected > len(playlists):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    selected_playlist = playlists[selected - 1][0]

    # 플레이리스트_음악에서 MNo 조회
    cursor.execute("""
        SELECT MNo
        FROM 플레이리스트_음악
        WHERE 이름 = %s AND UNo = %s
    """, (selected_playlist, userNumber))
    music_numbers = cursor.fetchall()

    if not music_numbers:
        print(f"\n'{selected_playlist}' 플레이리스트에 저장된 음악이 없습니다.\n")
        time.sleep(1)
        return
    
    print(f"\n'{selected_playlist}' 플레이리스트의 음악 목록:")
    music_numbers = [mno[0] for mno in music_numbers]  # 리스트로 변환
    query = f"""
        SELECT 
            음악.가수이름, 
            음악.제목, 
            GROUP_CONCAT(피처링.이름 SEPARATOR ', ') AS 피처링정보
        FROM 음악
        LEFT JOIN 피처링 ON 음악.MNumber = 피처링.MNo
        WHERE 음악.MNumber IN ({', '.join(map(str, music_numbers))})
        GROUP BY 음악.MNumber, 음악.가수이름, 음악.제목
    """
    cursor.execute(query)
    music_list = cursor.fetchall()

    for idx, (singer_name, title, featuring) in enumerate(music_list, start=1):
        featuring_text = f" (feat. {featuring})" if featuring else ""
        print(f"{idx}. {title} - {singer_name}{featuring_text}")

    print("0. 이전 메뉴로 돌아가기\n")

    selected = int(input("음악 번호를 선택하세요: "))

    if selected == 0:
        return
    elif selected < 1 or selected > len(music_numbers):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    selected_music = music_numbers[selected - 1]
    Music(userNumber, selected_music)

def createPlaylist(userNumber):
    print("\n플레이 리스트 생성하기\n")
    time.sleep(1)
    # 현재 플레이리스트 개수 확인
    cursor.execute("""
        SELECT COUNT(DISTINCT 이름) 
        FROM 플레이리스트 
        WHERE UNo = %s
    """, (userNumber,))
    current_count = cursor.fetchone()[0]

    # 프리미엄 상태 확인
    cursor.execute("SELECT COUNT(*) FROM 프리미엄 WHERE UNo = %s", (userNumber,))
    premium_status = cursor.fetchone()[0]

    # 최대 플레이리스트 개수 설정 (프리미엄: 3개, 일반: 2개)
    max_playlists = 3 if premium_status > 0 else 2

    if current_count >= max_playlists:
        print("플레이 리스트 개수를 초과했습니다. 더 이상 생성할 수 없습니다.\n")
        time.sleep(1)
        return
    
    playlist_name = input("플레이 리스트 이름 : ").strip()

    # 중복 확인
    cursor.execute("""
        SELECT COUNT(*) 
        FROM 플레이리스트
        WHERE UNo = %s AND 이름 = %s
    """, (userNumber, playlist_name))
    existing_playlist = cursor.fetchone()[0]

    if existing_playlist > 0:
        print("\n이미 존재하는 플레이 리스트 이름입니다. 다른 이름을 입력하세요.\n")
        time.sleep(1)
        return

    # 새로운 플레이리스트 추가
    cursor.execute("""
        INSERT INTO 플레이리스트 (이름, UNo)
        VALUES (%s, %s)
    """, (playlist_name, userNumber))
    db.commit()
    print(f"\n'{playlist_name}' 플레이 리스트가 성공적으로 생성되었습니다.\n")
    time.sleep(1)
    
def deletePlaylist(userNumber):
    print("\n플레이 리스트 삭제하기\n")
    time.sleep(1)
    # 사용자 플레이 리스트 조회
    cursor.execute("""
        SELECT 이름 
        FROM 플레이리스트 
        WHERE UNo = %s
    """, (userNumber,))
    playlists = cursor.fetchall()

    # 플레이 리스트가 없으면 종료
    if not playlists:
        print("삭제할 플레이 리스트가 없습니다.\n")
        time.sleep(1)
        return
    
    # 사용자 플레이 리스트 출력
    print("----- 내 플레이 리스트 -----")
    for idx, (playlist_name,) in enumerate(playlists, start=1):
        print(f"{idx}. {playlist_name}")

    # 삭제할 플레이 리스트 선택
    choice = int(input("\n삭제할 플레이 리스트 번호를 입력하세요: "))
    if choice < 1 or choice > len(playlists):
        print("\n잘못된 번호입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return
    
    playlist_name = playlists[choice - 1][0]

    confirm = input(f"\n'{playlist_name}' 플레이 리스트를 삭제하시겠습니까? (Y/N): ").upper()
    if confirm == "Y":
        # 플레이 리스트 삭제
        cursor.execute("""
            DELETE FROM 플레이리스트 
            WHERE UNo = %s AND 이름 = %s
        """, (userNumber, playlist_name))
        db.commit()
        print(f"\n'{playlist_name}' 플레이 리스트가 성공적으로 삭제되었습니다.\n")
        time.sleep(1)
    else:
        print("\n삭제가 취소되었습니다.\n")
        time.sleep(1)

def deleteMusicInPlaylist(userNumber):
    # 사용자 플레이리스트 조회
    cursor.execute("""
        SELECT DISTINCT 이름
        FROM 플레이리스트
        WHERE UNo = %s
    """, (userNumber,))
    playlists = cursor.fetchall()

    if not playlists:
        print("\n내 플레이리스트가 없습니다.\n")
        time.sleep(1)
        return
    
    cursor.execute("SELECT 닉네임 FROM 사용자 WHERE UNumber = %s", (userNumber,))
    result = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM 프리미엄 WHERE UNo = %s", (userNumber,))
    premium_status = cursor.fetchone()[0]
    nickname = result[0]
    if premium_status > 0:
        print(f"\n사용자 : {nickname} (Premium) 플레이 리스트")
    else:
        print(f"\n사용자 : {nickname} 플레이 리스트")
    for idx, (playlist_name,) in enumerate(playlists, start=1):
        print(f"{idx}. {playlist_name}")
    print("0. 이전 메뉴로 돌아가기\n")
    selected = int(input("플레이 리스트 번호를 선택하세요: "))

    if selected == 0:
        return
    elif selected < 1 or selected > len(playlists):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    selected_playlist = playlists[selected - 1][0]

    # 플레이리스트_음악에서 MNo 조회
    cursor.execute("""
        SELECT MNo
        FROM 플레이리스트_음악
        WHERE 이름 = %s AND UNo = %s
    """, (selected_playlist, userNumber))
    music_numbers = cursor.fetchall()

    if not music_numbers:
        print(f"\n'{selected_playlist}' 플레이리스트에 저장된 음악이 없습니다.\n")
        time.sleep(1)
        return
    
    print(f"\n'{selected_playlist}' 플레이리스트의 음악 목록:")
    music_numbers = [mno[0] for mno in music_numbers]  # 리스트로 변환
    query = f"""
        SELECT 
            음악.MNumber,
            음악.가수이름,
            음악.제목,
            GROUP_CONCAT(피처링.이름 SEPARATOR ', ') AS 피처링정보
        FROM 음악
        LEFT JOIN 피처링 ON 음악.MNumber = 피처링.MNo
        WHERE 음악.MNumber IN ({', '.join(map(str, music_numbers))})
        GROUP BY 음악.MNumber, 음악.가수이름, 음악.제목
    """
    cursor.execute(query)
    music_list = cursor.fetchall()

    for idx, (m_number, singer_name, title, featuring) in enumerate(music_list, start=1):
        featuring_text = f" (feat. {featuring})" if featuring else ""
        print(f"{idx}. {title} - {singer_name}{featuring_text}")

    print("0. 이전 메뉴로 돌아가기\n")

    selected = int(input("음악 번호를 선택하세요: "))

    if selected == 0:
        return
    elif selected < 1 or selected > len(music_list):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    selected_music = music_list[selected - 1][0]
    confirm = input(f"\n'{selected_playlist}' 플레이리스트에서 선택한 음악을 삭제하시겠습니까? (Y/N): ").strip().upper()
    if confirm == "Y":
        # 선택한 음악을 삭제
        cursor.execute("""
            DELETE FROM 플레이리스트_음악
            WHERE 이름 = %s AND UNo = %s AND MNo = %s
        """, (selected_playlist, userNumber, selected_music))
        db.commit()

        print(f"\n'{selected_playlist}' 플레이리스트에서 선택한 음악이 삭제되었습니다.\n")
        time.sleep(1)
    else:
        print("\n삭제가 취소되었습니다.\n")
        time.sleep(1)

def findPlaylist(userNumber):
    print("\n-----플레이 리스트 검색 -----")
    
    # 키워드 입력
    keyword = input("키워드를 입력하세요: ").strip()
    
    if not keyword:
        print("\n입력된 키워드가 없습니다. 다시 시도하세요.\n")
        time.sleep(1)
        return
    
    # 플레이리스트 이름과 사용자 닉네임 검색
    cursor.execute("""
        SELECT DISTINCT 플레이리스트.이름, 사용자.닉네임
        FROM 플레이리스트
        JOIN 사용자 ON 플레이리스트.UNo = 사용자.UNumber
        WHERE 플레이리스트.이름 LIKE %s
        LIMIT 5
    """, (f'%{keyword}%',))
    search_results = cursor.fetchall()
    
    if not search_results:
        print("\n일치하는 플레이 리스트가 없습니다.\n")
        time.sleep(1)
        return
    
    # 검색된 플레이리스트 출력
    print("\n----- 검색 결과 -----")
    for idx, (playlist_name, nickname) in enumerate(search_results, start=1):
        print(f"{idx}. {playlist_name} - {nickname}")
    print("0. 이전 메뉴로 돌아가기\n")
    
    # 사용자 입력
    selected = int(input("플레이 리스트 번호를 선택하세요: "))
    
    if selected == 0:
        return
    elif selected < 1 or selected > len(search_results):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 선택한 플레이리스트 정보 가져오기
    selected_playlist, selected_nickname = search_results[selected - 1]
    print(f"\n'{selected_playlist}' - {selected_nickname}님의 플레이리스트입니다.\n")
    
    # 플레이리스트_음악에서 MNo 조회
    cursor.execute("""
        SELECT MNo
        FROM 플레이리스트_음악
        WHERE 이름 = %s
    """, (selected_playlist,))
    music_numbers = cursor.fetchall()

    if not music_numbers:
        print(f"\n'{selected_playlist}' 플레이리스트에 저장된 음악이 없습니다.\n")
        time.sleep(1)
        return
    
    print(f"\n'{selected_playlist}' 플레이리스트의 음악 목록:")
    music_numbers = [mno[0] for mno in music_numbers]  # 리스트로 변환
    query = f"""
        SELECT 
            음악.MNumber,
            음악.가수이름,
            음악.제목,
            GROUP_CONCAT(피처링.이름 SEPARATOR ', ') AS 피처링정보
        FROM 음악
        LEFT JOIN 피처링 ON 음악.MNumber = 피처링.MNo
        WHERE 음악.MNumber IN ({', '.join(map(str, music_numbers))})
        GROUP BY 음악.MNumber, 음악.가수이름, 음악.제목
    """
    cursor.execute(query)
    music_list = cursor.fetchall()
    
    # 플레이리스트 음악 출력
    for idx, (m_number, singer_name, title, featuring) in enumerate(music_list, start=1):
        featuring_text = f" (feat. {featuring})" if featuring else ""
        print(f"{idx}. {title} - {singer_name}{featuring_text}")
    
    print("0. 이전 메뉴로 돌아가기\n")
    
    # 음악 선택
    selected_music_idx = int(input("음악 번호를 선택하세요: "))
    
    if selected_music_idx == 0:
        return
    elif selected_music_idx < 1 or selected_music_idx > len(music_list):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return

    # 선택한 음악 번호 가져오기
    selected_music = music_list[selected_music_idx - 1][0]
    Music(userNumber, selected_music)

def Premium(userNumber):
    while True:
        print("\n-----프리미엄 메뉴-----")
        cursor.execute("SELECT 닉네임 FROM 사용자 WHERE UNumber = %s", (userNumber,))
        result = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM 프리미엄 WHERE UNo = %s", (userNumber,))
        premium_status = cursor.fetchone()[0]
        nickname = result[0]
        if premium_status > 0:
            print(f"사용자 : {nickname} (Premium)")
        else:
            print(f"사용자 : {nickname}")
        print("1. 프리미엄 등록하기")
        print("2. 프리미엄 해제하기")
        print("0. 이전 메뉴로 돌아가기\n")

        sel = int(input("입력 : "))
        if sel == 1:
            registerPremium(userNumber)
        elif sel == 2:
            unregisterPremium(userNumber)
        elif sel == 0:
            break
        else:
            print("잘못된 입력입니다.\n")
            time.sleep(1)

def registerPremium(userNumber):
    print("\n프리미엄 등록하기")
    time.sleep(1)
    confirm = input("결제하시겠습니까? (Y/N): ").upper()

    if confirm == "Y":
        current_date = datetime.now().date()  # 현재 날짜 가져오기
        # 프리미엄 테이블에 데이터 삽입
        cursor.execute("""
            INSERT INTO 프리미엄 (결제날짜, UNo)
            VALUES (%s, %s)
        """, (current_date, userNumber))
        db.commit()  # 변경 사항 저장
        print("\n프리미엄이 성공적으로 등록되었습니다.")
        time.sleep(1)
        print(f"결제 날짜: {current_date}\n")
    else:
        print("\n프리미엄 등록이 취소되었습니다.\n")
        time.sleep(1)

def unregisterPremium(userNumber):
    print("\n프리미엄 해제하기\n")
    time.sleep(1)
    flag = 0
    # 플레이리스트 이름을 리스트에 저장
    cursor.execute("""
        SELECT DISTINCT 이름
        FROM 플레이리스트
        WHERE UNo = %s
    """, (userNumber,))
    playlist_names = [row[0] for row in cursor.fetchall()]  # 플레이리스트 이름 리스트

    if len(playlist_names) > 2:
        print(f"플레이 리스트가 {len(playlist_names)}개 있습니다. 플레이 리스트를 정리하세요.\n")
        time.sleep(1)
        flag = 1

    # 각 플레이리스트별 음악 개수를 확인
    for playlist_name in playlist_names:
        cursor.execute("""
            SELECT COUNT(MNo)
            FROM 플레이리스트_음악
            WHERE 이름 = %s AND UNo = %s
        """, (playlist_name, userNumber))
        music_count = cursor.fetchone()[0]

        if music_count > 3:
            print(f"플레이 리스트 '{playlist_name}'에 음악이 {music_count}개 있습니다. 음악을 정리하세요.\n")
            time.sleep(1)
            flag = 1

    if flag == 1:
        return
    
    cursor.execute("DELETE FROM 프리미엄 WHERE UNo = %s", (userNumber,))
    db.commit()
    print("프리미엄이 성공적으로 해제되었습니다.\n")
    time.sleep(1)

def adminSignUp():
    print("관리자 회원가입을 시작합니다")
    time.sleep(1)

    a_number = int(input("관리자 번호 : "))

     # 중복 확인
    cursor.execute("SELECT COUNT(*) FROM 관리자 WHERE ANumber = %s", (a_number,))
    count = cursor.fetchone()[0]
    if count > 0:
        print("\n중복된 관리자 번호입니다. 다른 번호를 입력하세요.\n")
        time.sleep(1)
        return

    name = input("이름 : ")
    gender = input("성별 (M/F) : ").upper()
    birth_date = input("생년월일 (YYYY-MM-DD) : ")
    nickname = input("닉네임 : ")
    email = input("메일주소 : ")
    address = input("집주소 : ")
    phone_number = input("전화번호 (예: 010-1234-5678) : ")
    time.sleep(1)

    # 입력값 확인
    print("\n입력한 정보:")
    print(f"관리자 번호 : {a_number}")
    print(f"이름 : {name}")
    print(f"성별 : {gender}")
    print(f"생년월일 : {birth_date}")
    print(f"닉네임 : {nickname}")
    print(f"메일주소 : {email}")
    print(f"집주소 : {address}")
    print(f"전화번호 : {phone_number}")

    confirm = input("위 정보를 저장하시겠습니까? (Y/N): ").upper()
    if confirm == "Y":
        # 데이터베이스에 INSERT
        cursor.execute("""
            INSERT INTO 관리자 (ANumber, 이름, 성별, 생년월일, 닉네임, 메일주소, 집주소, 전화번호)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (a_number, name, gender, birth_date, nickname, email, address, phone_number))
        db.commit()
        print("\n새로운 관리자가 성공적으로 추가되었습니다.\n")
        time.sleep(1)
    else:
        print("\n회원가입이 취소되었습니다.\n")
        time.sleep(1)

def Music(userNumber, selected_music):
    while True:
        # 음악 정보 조회
        cursor.execute("""
            SELECT 제목, 가수이름, 좋아요수, 댓글개수
            FROM 음악
            WHERE MNumber = %s
        """, (selected_music,))
        music_info = cursor.fetchone()

        if not music_info:
            print("\n음악 정보를 찾을 수 없습니다.\n")
            time.sleep(1)
            return
        
        title, singer_name, likes, comments = music_info
        print(f"\n노래 제목: {title}")
        print(f"가수: {singer_name}")
        print(f"좋아요 수: {likes}")
        print(f"댓글 수: {comments}")

        # 피처링 정보 조회
        cursor.execute("""
            SELECT 이름
            FROM 피처링
            WHERE MNo = %s
        """, (selected_music,))
        featuring_artists = cursor.fetchall()

        if featuring_artists:
            featuring_names = ", ".join(artist[0] for artist in featuring_artists)
            print(f"(feat. {featuring_names})")

        print("\n-----메뉴-----")
        print("1. 좋아요")
        print("2. 댓글")
        print("3. 플레이리스트에 추가하기")
        print("0. 이전 메뉴로 돌아가기\n")

        selected = int(input("선택: "))

        if selected == 0:
            return
        elif selected == 1:
            Like(userNumber, selected_music)
        elif selected == 2:
            Comment(userNumber, selected_music)
        elif selected == 3:
            addMusic2Playlist(userNumber, selected_music)
        else:
            print("잘못된 입력입니다.\n")
            time.sleep(1)

def Like(userNumber, selected_music):
    # 좋아요 상태 확인
    cursor.execute("""
        SELECT COUNT(*)
        FROM 좋아요
        WHERE UNo = %s AND MNo = %s
    """, (userNumber, selected_music))
    like_exists = cursor.fetchone()[0]

    if like_exists > 0:
        # 이미 좋아요를 눌렀으면 취소
        print("\n좋아요를 취소합니다.")
        time.sleep(1)
        cursor.execute("""
            DELETE FROM 좋아요
            WHERE UNo = %s AND MNo = %s
        """, (userNumber, selected_music))
        
        # 음악 테이블의 좋아요 수 감소
        cursor.execute("""
            UPDATE 음악
            SET 좋아요수 = 좋아요수 - 1
            WHERE MNumber = %s
        """, (selected_music,))
    else:
        # 좋아요 누르기
        print("\n좋아요를 누릅니다.")
        time.sleep(1)
        cursor.execute("""
            INSERT INTO 좋아요 (UNo, MNo)
            VALUES (%s, %s)
        """, (userNumber, selected_music))
        
        # 음악 테이블의 좋아요 수 증가
        cursor.execute("""
            UPDATE 음악
            SET 좋아요수 = 좋아요수 + 1
            WHERE MNumber = %s
        """, (selected_music,))

    db.commit()
    print("\n좋아요 상태가 변경되었습니다.\n")
    time.sleep(1)

def Comment(userNumber, selected_music):
    while True:
        print("\n-----댓글 메뉴-----")
        print("1. 모든 댓글 보기")
        print("2. 댓글 작성하기")
        print("0. 이전 메뉴로 돌아가기\n")

        selected = int(input("선택: "))

        if selected == 0:
            return
        elif selected == 1:
            viewComments(selected_music)
        elif selected == 2:
            writeComment(userNumber, selected_music)
        else:
            print("\n잘못된 입력입니다. 다시 시도하세요.\n")
            time.sleep(1)

def viewComments(selected_music):
    cursor.execute("""
        SELECT 날짜, UNo, 내용
        FROM 댓글
        WHERE MNo = %s
        ORDER BY 날짜 ASC
    """, (selected_music,))
    comments = cursor.fetchall()

    if not comments:
        print("\n댓글이 없습니다.\n")
        time.sleep(1)
        return

    print("\n-----댓글 목록-----")
    for idx, (date, user_no, content) in enumerate(comments, start=1):
        # 사용자 테이블에서 닉네임 가져오기
        cursor.execute("""
            SELECT 닉네임
            FROM 사용자
            WHERE UNumber = %s
        """, (user_no,))
        nickname = cursor.fetchone()[0]

        # 댓글 출력
        print(f"{idx}. {nickname} ({date}): {content}")

def writeComment(userNumber, selected_music):
    content = input("\n댓글 내용을 입력하세요: ").strip()
    current_date = datetime.now().date()  # 현재 날짜 가져오기
    if not content:
        print("\n댓글 내용이 비어 있습니다. 다시 시도하세요.\n")
        time.sleep(1)
        return
    
    # 댓글 데이터 삽입
    cursor.execute("""
        INSERT INTO 댓글 (날짜, UNo, MNo, 내용)
        VALUES (%s, %s, %s, %s)
    """, (current_date, userNumber, selected_music, content))

    # 댓글 개수 증가
    cursor.execute("""
            UPDATE 음악
            SET 댓글개수 = 댓글개수 + 1
            WHERE MNumber = %s
        """, (selected_music,))
    
    db.commit()
    print("\n댓글이 성공적으로 작성되었습니다.\n")
    time.sleep(1)

def addMusic2Playlist(userNumber, selected_music):
    # 사용자 플레이리스트 이름 가져오기
    cursor.execute("""
        SELECT DISTINCT 이름
        FROM 플레이리스트
        WHERE UNo = %s
    """, (userNumber,))
    playlists = cursor.fetchall()

    if not playlists:
        print("\n추가할 플레이리스트가 없습니다. 먼저 플레이리스트를 생성하세요.\n")
        time.sleep(1)
        return

    print("\n내 플레이리스트:")
    for idx, (playlist_name,) in enumerate(playlists, start=1):
        print(f"{idx}. {playlist_name}")
    print("0. 이전 메뉴로 돌아가기\n")

    selected = int(input("음악을 추가할 플레이리스트 번호를 선택하세요: "))

    if selected == 0:
        return

    if selected < 1 or selected > len(playlists):
        print("\n잘못된 입력입니다. 다시 시도하세요.\n")
        time.sleep(1)
        return
    
    # 선택한 플레이리스트 이름
    selected_playlist = playlists[selected - 1][0]

    # 프리미엄 상태 확인
    cursor.execute("SELECT COUNT(*) FROM 프리미엄 WHERE UNo = %s", (userNumber,))
    premium_status = cursor.fetchone()[0]

    # 최대 음악 개수 설정 (프리미엄: 5개, 일반: 3개)
    max_songs = 5 if premium_status > 0 else 3

    # 현재 플레이리스트에 저장된 음악 개수 확인
    cursor.execute("""
        SELECT COUNT(*)
        FROM 플레이리스트_음악
        WHERE 이름 = %s AND UNo = %s
    """, (selected_playlist, userNumber))
    current_music_count = cursor.fetchone()[0]

    if current_music_count >= max_songs:
        print(f"\n'{selected_playlist}' 플레이리스트에 더 이상 추가할 수 없습니다. 최대 {max_songs}곡까지 저장 가능합니다.\n")
        time.sleep(1)
        return
    
    # 중복 확인
    cursor.execute("""
        SELECT COUNT(*)
        FROM 플레이리스트_음악
        WHERE 이름 = %s AND UNo = %s AND MNo = %s
    """, (selected_playlist, userNumber, selected_music))
    is_duplicate = cursor.fetchone()[0]

    if is_duplicate > 0:
        print(f"\n'{selected_playlist}' 플레이리스트에 이미 이 음악이 있습니다.\n")
        time.sleep(1)
        return
    
    # 노래 제목 조회
    cursor.execute("""
        SELECT 제목
        FROM 음악
        WHERE MNumber = %s
    """, (selected_music,))
    music_title = cursor.fetchone()

    music_title = music_title[0]

    # 음악 추가
    cursor.execute("""
        INSERT INTO 플레이리스트_음악 (이름, UNo, MNo)
        VALUES (%s, %s, %s)
    """, (selected_playlist, userNumber, selected_music))
    db.commit()

    print(f"\n'{music_title}' 음악이 '{selected_playlist}' 플레이리스트에 추가되었습니다.\n")
    time.sleep(1)

main_menu()