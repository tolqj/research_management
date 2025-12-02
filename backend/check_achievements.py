"""检查成果数据"""
from database import SessionLocal
from models import Achievement

db = SessionLocal()

try:
    achievements = db.query(Achievement).all()
    print(f"总共 {len(achievements)} 个成果\n")
    
    for a in achievements:
        print(f"ID: {a.id}")
        print(f"  类型: {a.achievement_type}")
        print(f"  名称: {a.title}")
        print(f"  证书编号: {repr(a.certificate_no)} (类型: {type(a.certificate_no).__name__})")
        print(f"  所有人: {a.owner}")
        print(f"  完成日期: {a.completion_date}")
        print()
        
finally:
    db.close()
