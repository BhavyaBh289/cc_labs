const express = require('express');
const app = express();
const axios = require('axios');

// Apache server URLs
const apacheServers = [
	"http://192.168.122.5",
	"http://192.168.122.203"
];

// Track the current Apache server index
let currentApacheServerIndex = 0;

const handleApacheRequest = async (req, res) => {
    const { method, url, headers, body } = req;

    const currentServerUrl = apacheServers[currentApacheServerIndex];

    try {
        const response = await axios({
            url: `${currentServerUrl}${url}`,
            method: method,
            headers: headers,
            data: body
        });
        res.send(response.data);
    } catch (error) {
        console.error('Error fetching data from Apache server:', error);
        res.status(500).send('Server error');
    }
};

app.use((req, res) => {
    handleApacheRequest(req, res);
});

const PORT = process.env.PORT || 8090;
app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
