import time
import google.generativeai as genai
from config import GENAI_API_KEY, MODEL_NAME, MAX_RETRIES, RETRY_DELAY
from utils.error_handling import AIError

class AIService:
    """Service for AI integration and prompt management"""
    
    def __init__(self):
        self.model = None
        self.initialized = False
    
    def initialize(self):
        """Initialize the AI model"""
        try:
            genai.configure(api_key=GENAI_API_KEY)
            self.model = genai.GenerativeModel(MODEL_NAME)
            self.initialized = True
            print("Gemini model initialized successfully")
        except Exception as e:
            print(f"Error initializing Gemini model: {e}")
            self.initialized = False
            raise AIError(f"Failed to initialize AI model: {str(e)}")
    
    def generate_code(self, prompt: str) -> str:
        """Generate Python code using Gemini"""
        if not self.initialized:
            self.initialize()
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise AIError(f"Error generating code: {str(e)}")
    
    def process_query(self, query: str, ifc_file_path: str) -> str:
        """Process a query about an IFC file"""
        from services.ifc_service import IFCService
        from utils.security import clean_code, execute_code
        
        ifc_service = IFCService()
        
        # Generate Python code using Gemini
        prompt = f"""
        You are an IFC expert Python developer. Generate code to analyze an IFC file using ifcopenshell.
        Follow these strict rules:
        1. Only use ifcopenshell and standard libraries
        2. Use the pre-loaded 'ifc_file' variable (do not open the file again or modify it)
        3. Store final results in a variable named 'result'
        4. Never modify the original IFC file
        5. Handle potential errors with try/except blocks
        6. Return plain text without markdown or code block delimiters
        7. Ensure the code is complete and executable
        8. DO NOT include any backticks (```) in your response
        9. DO NOT attempt to redefine the ifc_file variable
        10. DO NOT use exec() or similar functions
        
        Important IFC Knowledge:
        - Use ifcopenshell's built-in methods like ifc_file.by_type(), ifc_file.get_entity_by_guid()
        - To get property sets, use ifcopenshell.util.element.get_psets() function on an element
        - Search for properties in psets (property sets) for cost/price information
        - In IFC, pricing can be stored in various ways: in Pset_CostItem, or custom psets with properties like "Cost", "Price", etc.
        - For buildings or units, look at property sets associated with IfcBuilding, IfcBuildingStorey, or IfcSpace elements
        
        Query: {query}
        """
        
        # Generate and execute code
        for attempt in range(MAX_RETRIES + 1):
            try:
                # Generate code
                code = self.generate_code(prompt)
                if code.startswith("Error"):
                    print(f"Attempt {attempt + 1}: {code}")
                    time.sleep(RETRY_DELAY)
                    continue
                
                # Clean the code
                code = clean_code(code)
                
                print(f"\nGenerated Code (Attempt {attempt + 1}):\n{code}")
                
                # Load the IFC file
                ifc_file = ifc_service.load_file(ifc_file_path)
                
                # Execute the code
                result = execute_code(code, ifc_file)
                if "Error" not in result and "Traceback" not in result:
                    return result  # Return the final result
                else:
                    print(f"Attempt {attempt + 1}: Code execution failed.")
                    if attempt < MAX_RETRIES:
                        # Improve the prompt based on the error
                        prompt += f"\n\nPrevious code had errors: {result}\nPlease fix these issues. For property sets, use ifcopenshell.util.element module if available, or carefully navigate the IFC structure using proper attribute checking."
                        time.sleep(RETRY_DELAY)
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES:
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise AIError(f"Failed after {MAX_RETRIES} attempts. Final error: {e}")

# Create a singleton instance
ai_service = AIService() 