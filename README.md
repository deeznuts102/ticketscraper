# ticketscraper

[Latest files]()


## Using datamodel-code-generator to generate models from JSON

1. Download JSON file locally e.g. as `result.json`
2. Run `datamodel-code-generator` module to generate models:
```bash
datamodel-codegen --input result.json --input-file-type json --output models/res.py --class-name Event  --snake-case-field   --use-schema-description --use-title-as-name --target-python-version 3.9
```
