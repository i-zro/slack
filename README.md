## ca_bot

### 🤐 secrets 관리
1. 프로젝트의 Settings 탭으로 이동합니다.

2. 좌측 사이드바에서 Secrets 섹션을 찾고, Actions를 클릭합니다.

3. New repository secret 버튼을 클릭하여 새로운 시크릿을 추가합니다.

4. 다음 시크릿들을 추가하였습니다:

  - GCP_PROJECT_ID: Google Cloud 프로젝트 ID.
  
  - GCP_SA_KEY: Google Cloud 서비스 계정 키 (JSON 형태). Base64로 인코딩되어야 하기 때문에, `base64 <filename.json>` 명령어를 사용하여 인코딩하였습니다.
  
  - SLACK_BOT_TOKEN: Slack Bot Token.
