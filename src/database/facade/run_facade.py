from database.database import with_db_session
from database.models.dim_files import DimFiles
from database.models.dim_models import DimModels
from database.models.dim_prompts import DimPrompts


class RunFacade:
    
    @with_db_session
    def save_run(self, pdf_path: str, model_name: str, system_prompt: str, user_prompt: str, db=None):
        file_record = DimFiles(filepath=pdf_path)
        db.add(file_record)
        
        model_record = DimModels(name=model_name)
        db.add(model_record)
        
        prompt_record = DimPrompts(system_prompt=system_prompt, user_prompt=user_prompt)
        db.add(prompt_record)