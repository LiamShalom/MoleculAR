import os
import json
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Handles database operations for storing analysis results
    """
    
    def __init__(self):
        self.db_type = os.getenv('DATABASE_TYPE', 'file')  # 'file', 'supabase', 'postgresql'
        self.initialize_database()
    
    def initialize_database(self):
        """
        Initialize database connection
        """
        try:
            if self.db_type == 'file':
                # Use file-based storage for demo
                self.data_dir = 'data'
                os.makedirs(self.data_dir, exist_ok=True)
                logger.info("Initialized file-based database")
                
            elif self.db_type == 'supabase':
                # Initialize Supabase connection
                from supabase import create_client, Client
                url = os.getenv('SUPABASE_URL')
                key = os.getenv('SUPABASE_KEY')
                self.supabase: Client = create_client(url, key)
                logger.info("Initialized Supabase database")
                
            elif self.db_type == 'postgresql':
                # Initialize PostgreSQL connection
                import psycopg2
                self.conn = psycopg2.connect(
                    host=os.getenv('POSTGRES_HOST', 'localhost'),
                    database=os.getenv('POSTGRES_DB', 'molecular_analysis'),
                    user=os.getenv('POSTGRES_USER', 'postgres'),
                    password=os.getenv('POSTGRES_PASSWORD', 'password'),
                    port=os.getenv('POSTGRES_PORT', '5432')
                )
                self._create_tables()
                logger.info("Initialized PostgreSQL database")
                
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            self.db_type = 'file'  # Fallback to file storage
    
    def _create_tables(self):
        """
        Create database tables for PostgreSQL
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id VARCHAR(36) PRIMARY KEY,
                    input_type VARCHAR(20) NOT NULL,
                    molecular_data TEXT NOT NULL,
                    quantum_results JSONB,
                    properties JSONB,
                    ml_predictions JSONB,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
            cursor.close()
            
        except Exception as e:
            logger.error(f"Failed to create tables: {str(e)}")
    
    def store_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """
        Store analysis results in database
        """
        try:
            analysis_id = str(uuid.uuid4())
            
            if self.db_type == 'file':
                return self._store_in_file(analysis_id, analysis_data)
            elif self.db_type == 'supabase':
                return self._store_in_supabase(analysis_id, analysis_data)
            elif self.db_type == 'postgresql':
                return self._store_in_postgresql(analysis_id, analysis_data)
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
                
        except Exception as e:
            logger.error(f"Failed to store analysis: {str(e)}")
            return str(uuid.uuid4())  # Return a fallback ID
    
    def _store_in_file(self, analysis_id: str, analysis_data: Dict[str, Any]) -> str:
        """
        Store analysis in file system
        """
        try:
            file_path = os.path.join(self.data_dir, f"{analysis_id}.json")
            
            with open(file_path, 'w') as f:
                json.dump(analysis_data, f, indent=2, default=str)
            
            logger.info(f"Stored analysis {analysis_id} in file")
            return analysis_id
            
        except Exception as e:
            logger.error(f"Failed to store in file: {str(e)}")
            raise
    
    def _store_in_supabase(self, analysis_id: str, analysis_data: Dict[str, Any]) -> str:
        """
        Store analysis in Supabase
        """
        try:
            result = self.supabase.table('analyses').insert({
                'id': analysis_id,
                'input_type': analysis_data.get('input_type'),
                'molecular_data': analysis_data.get('molecular_data'),
                'quantum_results': analysis_data.get('quantum_results'),
                'properties': analysis_data.get('properties'),
                'ml_predictions': analysis_data.get('ml_predictions'),
                'timestamp': analysis_data.get('timestamp')
            }).execute()
            
            logger.info(f"Stored analysis {analysis_id} in Supabase")
            return analysis_id
            
        except Exception as e:
            logger.error(f"Failed to store in Supabase: {str(e)}")
            raise
    
    def _store_in_postgresql(self, analysis_id: str, analysis_data: Dict[str, Any]) -> str:
        """
        Store analysis in PostgreSQL
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO analyses (id, input_type, molecular_data, quantum_results, properties, ml_predictions, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                analysis_id,
                analysis_data.get('input_type'),
                analysis_data.get('molecular_data'),
                json.dumps(analysis_data.get('quantum_results')),
                json.dumps(analysis_data.get('properties')),
                json.dumps(analysis_data.get('ml_predictions')),
                analysis_data.get('timestamp')
            ))
            self.conn.commit()
            cursor.close()
            
            logger.info(f"Stored analysis {analysis_id} in PostgreSQL")
            return analysis_id
            
        except Exception as e:
            logger.error(f"Failed to store in PostgreSQL: {str(e)}")
            raise
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve analysis results from database
        """
        try:
            if self.db_type == 'file':
                return self._get_from_file(analysis_id)
            elif self.db_type == 'supabase':
                return self._get_from_supabase(analysis_id)
            elif self.db_type == 'postgresql':
                return self._get_from_postgresql(analysis_id)
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
                
        except Exception as e:
            logger.error(f"Failed to get analysis: {str(e)}")
            return None
    
    def _get_from_file(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve analysis from file system
        """
        try:
            file_path = os.path.join(self.data_dir, f"{analysis_id}.json")
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Failed to get from file: {str(e)}")
            return None
    
    def _get_from_supabase(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve analysis from Supabase
        """
        try:
            result = self.supabase.table('analyses').select('*').eq('id', analysis_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"Failed to get from Supabase: {str(e)}")
            return None
    
    def _get_from_postgresql(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve analysis from PostgreSQL
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM analyses WHERE id = %s", (analysis_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return {
                    'id': result[0],
                    'input_type': result[1],
                    'molecular_data': result[2],
                    'quantum_results': json.loads(result[3]) if result[3] else None,
                    'properties': json.loads(result[4]) if result[4] else None,
                    'ml_predictions': json.loads(result[5]) if result[5] else None,
                    'timestamp': result[6].isoformat() if result[6] else None,
                    'created_at': result[7].isoformat() if result[7] else None
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get from PostgreSQL: {str(e)}")
            return None
    
    def get_recent_analyses(self, limit: int = 10) -> list:
        """
        Get recent analyses
        """
        try:
            if self.db_type == 'file':
                return self._get_recent_from_file(limit)
            elif self.db_type == 'supabase':
                return self._get_recent_from_supabase(limit)
            elif self.db_type == 'postgresql':
                return self._get_recent_from_postgresql(limit)
            else:
                return []
                
        except Exception as e:
            logger.error(f"Failed to get recent analyses: {str(e)}")
            return []
    
    def _get_recent_from_file(self, limit: int) -> list:
        """
        Get recent analyses from file system
        """
        try:
            files = []
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.data_dir, filename)
                    stat = os.stat(file_path)
                    files.append((stat.st_mtime, file_path))
            
            files.sort(reverse=True)
            recent_files = files[:limit]
            
            analyses = []
            for _, file_path in recent_files:
                with open(file_path, 'r') as f:
                    analysis = json.load(f)
                    analyses.append(analysis)
            
            return analyses
            
        except Exception as e:
            logger.error(f"Failed to get recent from file: {str(e)}")
            return []
    
    def _get_recent_from_supabase(self, limit: int) -> list:
        """
        Get recent analyses from Supabase
        """
        try:
            result = self.supabase.table('analyses').select('*').order('created_at', desc=True).limit(limit).execute()
            return result.data or []
            
        except Exception as e:
            logger.error(f"Failed to get recent from Supabase: {str(e)}")
            return []
    
    def _get_recent_from_postgresql(self, limit: int) -> list:
        """
        Get recent analyses from PostgreSQL
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM analyses ORDER BY created_at DESC LIMIT %s", (limit,))
            results = cursor.fetchall()
            cursor.close()
            
            analyses = []
            for result in results:
                analyses.append({
                    'id': result[0],
                    'input_type': result[1],
                    'molecular_data': result[2],
                    'quantum_results': json.loads(result[3]) if result[3] else None,
                    'properties': json.loads(result[4]) if result[4] else None,
                    'ml_predictions': json.loads(result[5]) if result[5] else None,
                    'timestamp': result[6].isoformat() if result[6] else None,
                    'created_at': result[7].isoformat() if result[7] else None
                })
            
            return analyses
            
        except Exception as e:
            logger.error(f"Failed to get recent from PostgreSQL: {str(e)}")
            return []
