from dataclasses import dataclass
import re

@dataclass
class Contact:
    last_name: str = None
    name: str = None
    middle_name: str = None
    organization: str = None
    work_phone: str = None  
    mobile_phone: str = None  

