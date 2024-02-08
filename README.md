## ca_bot

### 💾 디렉토리 구조

```
├── ./.github
│   └── ./.github/workflows
│       └── ./.github/workflows/deploy.yml
├── ./README.md
└── ./ca_bot
    ├── ./ca_bot/app.yaml
    ├── ./ca_bot/main.py
    └── ./ca_bot/requirements.txt
```

### 📢 기능

- 메시지에 선임, 책임, 팀장, 담당, 상무, 전무 포함하는 글자 있을 때 reaction
- 메시지가 CA, ca, CA!, ca!와 일치할 때 reaction

### 🤐 secrets 관리
1. 프로젝트의 Settings 탭으로 이동합니다.

2. 좌측 사이드바에서 Secrets 섹션을 찾고, Actions를 클릭합니다.

3. New repository secret 버튼을 클릭하여 새로운 시크릿을 추가합니다.

4. 다음 시크릿들을 추가하였습니다:

- GCP_PROJECT_ID: Google Cloud 프로젝트 ID.

- GCP_SA_KEY: Google Cloud 서비스 계정 키 (JSON 형태). Base64로 인코딩되어야 하기 때문에, `base64 <filename.json>` 명령어를 사용하여 인코딩하였습니다.

- SLACK_BOT_TOKEN: Slack Bot Token. ☠️

  - APP_YAML_CONTENT: GitHub Actions workflow에서 app.yaml 파일을 동적으로 생성. 이는 추후 구글 시크릿 매니저나 aws를 사용한다면 AWS 파라미터 스토어 사용해서 이렇게 파일을 굳이 동적으로 만들지 않고 가능함.
