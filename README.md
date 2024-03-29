## ca_bot

### 💾 디렉토리 구조

```
├── .github
│   └── workflows
│       └── deploy.yml
├── README.md
└── ca_bot
    ├── .gcloudignore
    ├── app
    │   ├── __init__.py
    │   ├── main.py
    │   ├── praise.py
    │   └── uplus_nim.py
    └── requirements.txt
```

### 🤚 사용법
사용을 원하는 채널에 `/invite @caca` 명령어를 입력

### 📢 기능

- 메시지에 선임, 책임, 팀장, 담당, 상무, 전무 포함하는 글자 있을 때 reaction
    - [240326] 보완사항 - '님들'이 뒤에 붙을 때는 trigger 되지 않도록 조정 (negative lookahead assertion (?!님들)을 사용)
    - [240326] 보완사항 - 봄날같은 인사, ‘~~~님’과 함께 시작해보세요! 에서 발언한 사람의 이름이 들어가는 게 부자연스러움. 호칭 앞에 있는 이름을 잡도록 변경
        - re.sub(r'<@\w+>', '', text)를 사용하여 입력 텍스트에서 Slack 사용자 멘션을 제거
    - [240328] '님들'을이 들어가는 경우 해당 단어 trigger_words 잡는 문장에서 아예 제거
    - [240328] firestore 저장과정 추가하자 너무 시간이 오래 걸려서 메시지 오류로 파악하고 두번 가는 (ack를 못잡는) 문제 발생. 문제 해결하고자 threading 사용. (더 좋은 방법이 있다면 somebody talk to me...)
    - [240329] '그룹장님' 추가, 모듈을 일부 잘못 불러와서 데이터 저장 안되는 이슈 있어서 고침
- 메시지가 CA, ca, CA!, ca!와 일치할 때 reaction
- 칭찬하기: 슬랙에서 `/칭찬하기 @유저명 칭찬내용` 입력하면 reaction 및 firestore에 칭찬 수발신자 저장 및 내용 저장

### 🤐 secrets 관리
1. 프로젝트의 Settings 탭으로 이동합니다.

2. 좌측 사이드바에서 Secrets 섹션을 찾고, Actions를 클릭합니다.

3. New repository secret 버튼을 클릭하여 새로운 시크릿을 추가합니다.

4. 다음 시크릿들을 추가하였습니다:

- GCP_PROJECT_ID: Google Cloud 프로젝트 ID.

- GCP_SA_KEY: Google Cloud 서비스 계정 키 (JSON 형태). Base64로 인코딩되어야 하기 때문에, `base64 <filename.json>` 명령어를 사용하여 인코딩하였습니다.

- SLACK_BOT_TOKEN: Slack Bot Token. ☠️

  - APP_YAML_CONTENT: GitHub Actions workflow에서 app.yaml 파일을 동적으로 생성. 이는 추후 구글 시크릿 매니저나 aws를 사용한다면 AWS 파라미터 스토어 사용해서 이렇게 파일을 굳이 동적으로 만들지 않고 가능함.

### 🤚 테스트 케이스
- 정재근 팀장님 안녕하세요
- @정재근 팀장님 안녕하세요
- 팀장님들 안녕하세요
- 
