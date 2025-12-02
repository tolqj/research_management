"""检查经费数据"""
from database import SessionLocal
from models import Fund

db = SessionLocal()
funds = db.query(Fund).all()
print(f"经费记录总数: {len(funds)}")
for f in funds[:10]:
    print(f"  - {f.expense_type}: ¥{f.amount:,.0f} (项目ID: {f.project_id}, 经办人: {f.handler})")
db.close()
