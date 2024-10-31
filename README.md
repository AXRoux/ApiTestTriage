# REST API Testing Tool 🔌

A powerful and user-friendly REST API testing and troubleshooting tool built with Streamlit. This tool helps developers test, monitor, and analyze API endpoints with ease.

## Features

- 🚀 **API Request Testing**
  - Support for GET, POST, PUT, DELETE, PATCH, and HEAD methods
  - JSON request body editor
  - Custom headers configuration
  - Request history tracking

- 🔒 **Authentication Support**
  - Basic Authentication
  - Bearer Token
  - OAuth2 integration

- 📊 **Response Analysis**
  - Beautiful response formatting
  - Performance metrics visualization
  - Status code indicators
  - Headers inspection

- 📝 **Request History**
  - Track all previous requests
  - Export history to JSON or CSV
  - Easy request replay

- 🔍 **Health Monitoring**
  - Automated endpoint health checks
  - Customizable check intervals
  - Response time tracking
  - Status history visualization

## Requirements

- Python 3.10 or higher
- Dependencies:
  - streamlit
  - requests
  - aiohttp
  - plotly

## Installation & Setup

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/username/rest-api-testing-tool
cd rest-api-testing-tool
```

2. Install the required dependencies:
```bash
pip install streamlit requests aiohttp plotly
```

3. Create a `.streamlit/config.toml` file with:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

4. Start the application:
```bash
streamlit run main.py
```

5. Access the application at `http://localhost:5000`

## Usage

1. Access the application through your browser
2. Enter your API endpoint details:
   - URL
   - HTTP method
   - Headers (in JSON format)
   - Request body (for POST/PUT/PATCH)
3. Click "Send Request" to test your API
4. View the response, performance metrics, and save configurations for later use

## Key Components

- **Request Configuration**
  - Easy-to-use form interface
  - Save and load request configurations
  - Authentication options

- **Response Viewer**
  - Formatted JSON/XML/HTML display
  - Response headers inspection
  - Status code indicators

- **Performance Metrics**
  - Response time tracking
  - Size measurements
  - Visual performance graphs

- **Health Monitoring**
  - Add multiple endpoints
  - Set custom check intervals
  - View real-time health status

## Troubleshooting

### Common Issues

1. **Application not starting:**
   - Ensure all dependencies are installed correctly
   - Check if port 5000 is available
   - Verify Python version compatibility

2. **Authentication issues:**
   - Double-check credentials format
   - Ensure OAuth2 token URL is accessible
   - Verify Bearer token format

3. **Request failures:**
   - Verify endpoint URL is correct and accessible
   - Check network connectivity
   - Validate JSON format in request body

### Error Messages

- `JSONDecodeError`: Check if your request body is valid JSON
- `Connection refused`: Verify the API endpoint is accessible
- `Invalid headers format`: Ensure headers are in correct JSON format

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Creator

Created by [Vance Poitier](https://www.linkedin.com/in/vance-poitier/)

## Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section above
2. Open an issue in the repository
3. Contact the creator via LinkedIn

---

Made with ❤️ using [Streamlit](https://streamlit.io/)
