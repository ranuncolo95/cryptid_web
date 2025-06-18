import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError


conn: Connection | None = None
curs: Cursor | None = None

def get_db(name: str|None = None, reset: bool = False):
    """Connect to SQLite database file"""
    global conn, curs
    
    if conn and not reset:
        return
    
    if conn:
        conn.close()
    
    if not name:
        # Get default path
        top_dir = Path(__file__).resolve().parents[0]  # repo top
        db_dir = top_dir / "db"
        db_name = "cryptid.db"
        
        # Ensure the db directory exists
        db_dir.mkdir(parents=True, exist_ok=True)
        
        db_path = str(db_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    
    try:
        conn = connect(name, check_same_thread=False)
        curs = conn.cursor()
    except Exception as e:
        raise RuntimeError(f"Failed to connect to database at {name}: {str(e)}")

get_db()