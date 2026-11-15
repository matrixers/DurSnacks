const app = require('./app');

// starts server
function startServer() {
    app.listen(8090, () => {
        console.log('Server is running on port 8090');
    });
}

// server disconnection or crash
app.on('error', (err) => {
    console.error('Server error occurred:', err);
    console.log('Attempting to restart the server...');
    setTimeout(startServer, 5000); // Restarts the after 5 seconds
});

// start server
startServer();