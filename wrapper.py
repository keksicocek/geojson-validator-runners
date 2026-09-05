import sys
import os
import json
from geojson_validator import validate_structure

def validate_single_file(file_path):
    filename = os.path.basename(file_path)
    validation_passed = True
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
            
        validation_result = validate_structure(geojson_data)
        
        if validation_result: 
            validation_passed = False
            for err_type, err_list in validation_result.items():
                errors.append(f"{err_type}: {str(err_list)}")

    except json.JSONDecodeError as e:
        validation_passed = False
        errors.append(f"{str(e)}")
    except Exception as e:
        validation_passed = False
        errors.append(f"{str(e)}")

    return {
        "fileName": filename,
        "format": "GEOJSON",
        "validationPassed": validation_passed,
        "errors": errors
    }

def main():
    if len(sys.argv) < 2:
        print("<vstup>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    tested_files = []

    if os.path.isdir(input_path):
        for root_dir, dirs, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(('.geojson', '.json')):
                    full_path = os.path.join(root_dir, file)
                    result = validate_single_file(full_path)
                    tested_files.append(result)
                    
    elif os.path.isfile(input_path):
        if input_path.lower().endswith(('.geojson', '.json')):
            result = validate_single_file(input_path)
            tested_files.append(result)
    else:
        print(f"{input_path}", file=sys.stderr)
        sys.exit(1)

    report = {
        "libraryName": "geojson-validator",
        "libraryVersion": "1.0.0",
        "testedFiles": tested_files
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
