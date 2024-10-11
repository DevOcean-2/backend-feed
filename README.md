# Backend Feed Service

## 개발 환경 세팅
1. virtural env 설정
    ```shell
   pip3 install virtualenv
   virtualenv .venv --python=python3.12
   source .venv/bin/activate
   ```
2. 패키지 설치
   ```shell
   pip3 install -r requirements.txt
   ```

## 개발
1. 브랜치
   - `<category>/<name>`의 네이밍 (e.g. `feat/photo-upload`, `fix/upload-bug`) ([카테고리 참고](https://github.com/pvdlg/conventional-changelog-metahub#commit-types)) 
2. 파일 수정 시 
   - lint 체크 후 메이져 이슈들은 수정 부탁드립니다. pylint 사용합니다.
   ```shell
   make lint
   ```
   - 패키지 체크
   ```shell
   make generate-requirements
   ```
3. 커밋
   - 한글로 쓰시던 영어로 쓰시던 편하신대로. `<category>: <message>` 형식만 지켜주세요
   - 옛날에 읽었던 [좋은 커밋 메세지 쓰는 법](https://chris.beams.io/posts/git-commit/)?? 입니다. 참고만 해주세요
4. Pull Request
   - PR = 1 커밋을 원칙으로 (pr 하나에 커밋이 여러 개면 리뷰가 힘들어요ㅜㅜ)
   - 사소한 내용일 경우 셀프 머지도 허용 
   - 머지 방식은 개인적으로 rebase merge를 선호합니다.