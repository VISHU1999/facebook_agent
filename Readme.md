# Facebook Comments Analyzer using Agents

This Python script analyzes comments on a Facebook page and hides comments that contain offensive words. It utilizes the [uagents](https://pypi.org/project/uagents/) library and the Facebook Graph API.

## Prerequisites

- Python 3.6 or above
- Facebook user access token with the `manage_pages` and `read_page_content` permissions
- Facebook page ID or name
- Offensive words list

## Installation

1. Clone this repository or download the `facebook_comments_analyzer.py` script file.

2. Install the required dependencies by running the following command:

   ```bash
   pip install request 
   pip install uagents
   ```

3. Create a `.env` file in the project directory and add the following environment variables:

   ```plaintext
   ACCESS_TOKEN=<your_facebook_access_token>
   PAGE=<facebook_page_name_or_id>
   OFFENSIVE_WORD=<comma_separated_offensive_words_list>
   POST_LIMIT=<optional_post_limit>
   COMMENTS_SINCE_MIN=<optional_comments_since_minutes>
   ```
   I have created a example env file you can copy and add your information there.
   I have already added offensive words if you wish to want to add somethings feel free to do 

   - `ACCESS_TOKEN`: Your Facebook user access token with the necessary permissions.
   - `PAGE`: The name or ID of the Facebook page you want to analyze.
   - `OFFENSIVE_WORD`: A comma-separated list of offensive words to consider for comment filtering.
   - `POST_LIMIT` (optional): The number of latest posts to retrieve and analyze comments from. Default is 1.
   - `COMMENTS_SINCE_MIN` (optional): The number of minutes ago to consider for analyzing comments. Default is 1.

## Usage

Run the script using the following command:

```bash
python facebook_comments_analyzer.py
```

The script will start analyzing the comments on the specified Facebook page and hide any comments that contain offensive words.

If the `PAGE` environment variable is not specified, the script will analyze comments on all Facebook pages associated with the user.

You can adjust the `POST_LIMIT` and `COMMENTS_SINCE_MIN` environment variables to modify the script's behavior.

## License

This project is licensed under the [MIT License](LICENSE).


Feel free to modify and enhance the script according to your specific needs. Make sure to follow the Facebook API guidelines and respect user privacy when using the script on real-world scenarios.
