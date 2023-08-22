# Project

> This repo has been populated by an initial template to help get you started. Please
> make sure to update the content to build a great experience for community-building.

As the maintainer of this project, please make a few updates:

- Improving this README.MD file to provide a great experience
- Updating SUPPORT.MD with content about this project's support experience
- Understanding the security reporting process in SECURITY.MD
- Remove this section from the README

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

# Pre-requisites 

Needs Python 3.10 or better.

(Can get from here: https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-10-on-ubuntu-18-04-and-20-04-lts/)


1. Enter a virtual environment with pip on conda
```
python3.11 -m venv venvname
source venvname/bin/activate
```

2. Install the requirements.txt with pip on conda
```
pip install -r requirements.txt
```

3. Set the secrect key
In the `app_traffic_analysis/strawman/` and `app_lifecycle_management/strawman/` folder:

Rename .env.template to .env

Set OPENAI_API_KEY to be an openAI API key in the .env file.
> Make sure that the OPENAI_API_KEY has credits

Note that by default we use [AzureOpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service-b) key, if you want to use non-Azure key, please select the following in `strawman/ai_model.py`
```
# Without Azure key
llm = OpenAI(
    model_name='text-davinci-003',
    temperature=0,
    max_tokens=2048,
    openai_api_key=OPENAI_API_KEY
   )
```


# Run two applications

## Traffic Analysis

1. To run with existing query
```
cd app_traffic_analysis/strawman
python test_with_golden.py
```
Results are logged in `strawman/logs/`

2. To add your own query with golden answer code
Add your {prompt, answer} pair in the following code. Node that the order of prompt and answers must match.
```
cd app_traffic_analysis/golden_answer_generator
python write_new_pair_to_df.py
```

3. Example to generate a new Network graph
Please check meaning of params in `mock_graph_data.py`.
```
cd app_traffic_analysis/strawman
python mock_graph_data.py --n=5 --v=5 --c=0.05 --o=data/graph_data/node5.json
```


If you want to load the new graph, change the floowing global variable in `strawman/test_with_golden.py` to the graph path you want.
```
OUTPUT_JSONL_PATH = 'logs/node10_log.jsonl'
GRAPH_PATH = "../data/graph_data/node10.json"
```


## Lifecycle management
We use [Google MALT data](https://github.com/google/malt-example-models) as an example of application use. The full data is avaliable in the original git repo.

For strawman showcase, we only extract a small set of original data due to LLMs token limit. The sampled data is stored in `app_lifecycle_management/data/malt-example-sample.txt`.

To run:
```
cd app_lifecycle_management/strawman
python test_with_golden.py
```