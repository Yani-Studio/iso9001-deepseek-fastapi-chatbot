#!/bin/bash
# ============================================================
# ISO 9001 완전 독립 파이프라인 (생성+튜닝+평가) 5트랙 자동화
# ============================================================

set -e
REMOTE="yani-studio"
LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)/iso_scripts"
REMOTE_DIR="/home/yani_studio/Desktop/iso"

echo "🔍 서버 연결 확인 중..."
if ! ssh -o BatchMode=yes -o ConnectTimeout=15 "$REMOTE" "echo OK" 2>/dev/null; then
    echo "❌ 서버 연결 실패. 서버가 켜져 있고 SSH 접속 가능한지 확인하세요."
    exit 1
fi
echo "✅ 서버 연결 OK"

echo ""
echo "📦 스크립트 배포 중..."
FILES="config.py step1_extract_pdf.py step2_generate_qa.py step3_finetune.py run_all_models.py step6_app.py step4_build_vectordb.py"
for f in $FILES; do
    if [ -f "$LOCAL_DIR/$f" ]; then
        scp -q "$LOCAL_DIR/$f" "$REMOTE:$REMOTE_DIR/$f"
        echo "  ✅ $f"
    fi
done

echo ""
echo "🚀 5트랙 파이프라인 실행 중 (백그라운드)..."
ssh "$REMOTE" "rm -f $REMOTE_DIR/pipeline_status.json 2>/dev/null && cd $REMOTE_DIR && nohup python3 run_all_models.py > pipeline.log 2>&1 &"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ 5개 모델별 완벽 독립 생성/튜닝 파이프라인이 시작되었습니다!"
echo "  이 작업은 모델별 수천 개의 QA 데이터를 생성하고 튜닝하므로"
echo "  최소 24시간 이상 소요될 수 있습니다. (서버 끄지 마세요!)"
echo ""
echo "  📝 실시간 로그 확인:"
echo "     ssh yani-studio 'tail -f $REMOTE_DIR/pipeline.log'"
echo "════════════════════════════════════════════════════════════"
