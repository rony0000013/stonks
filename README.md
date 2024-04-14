# Stonks App 📈📉

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stonks-stonks.streamlit.app)

## Features

- **Stock Summary**: Get a comprehensive overview of stocks, including daily price charts and essential information.
- **Multi-Language Support**: Access stock information in multiple languages, ensuring accessibility for a global audience.
- **News and Sentiment Analysis**: Stay up-to-date with recent news related to stocks, accompanied by sentiment analysis for better decision-making.
- **Customizable Date**: Users can customize the date to obtain stock information tailored to their specific needs.
- **LLM Model Selection**: Choose from various Large Language Models (LLMs) to generate stock information based on individual preferences.

## Getting Started

### Prerequisites - Python and Poetry, Stonks-worker deployed or running locally

To run the Stonks App locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/rony0000013/stonks.git
    ```

2. Install the dependencies:

    ```bash
    poetry install
    ```

3. Add stonks worker deployed link in `.streamlit/secrets.toml`

    ```bash
    url = "<your-deployment-link>
    ```
4. Run the app
    ```bash
    poetry run streamlit run main.py
    ```


## Contributing

Contributions to the Stonks App are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).


## Tech Stacks

- Streamlit for the easy-to-use web app framework.
- Cloudflare Workers for serverless computing.
- Workers AI for providing the language models.
- polygon.io for the stock market data API.
