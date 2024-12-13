const express = require('express');
const path = require('path');
const app = express();
const data = require('./load-and-vectorize-data');
const port = process.env.PORT || 3000;
let taskStatuses = {};

app.use(express.static(path.join(__dirname, 'public')));

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// TODO: Extend the application code

app.get('/submitOption', async (req, res) => {
    try {
        const query = req.query.o;

        if (query === '1' || query === '2') {
            
            console.log("Starting long-running operation for query:", query);
            const taskId = Date.now();
            taskStatuses[taskId] = 'pending';
            
            data.processOption(query).then(() => {
                taskStatuses[taskId] = 'completed';
                console.log("Task completed:", taskId);
            });

            res.json({ result: "Please wait while the vector index is created. This may take a while.", 
                       taskId: taskId, status: 'pending' });

        } else {

            const result = await data.processOption(query);
            res.json({result : result});

        }
    } catch (error) {
        console.error("Error processing option:", error);
        res.status(500).send("An error occurred while processing the request.");
    }
});

app.get('/submitQuery', async (req, res) => {
    try {

        const option = req.query.o;
        const query = req.query.q;

        if (option == '3') {

            const result = await data.doVectorSearch(query);

            // convert the array to a string for the client
            const resultString = result.join('\n'); 
            res.send({result: resultString});

        } else if (option == '4') {

            const result = await data.doGPTSearch(query);
            res.json({result : result});

        }
    } catch (error) {
        console.error("Error processing option:", error);
        res.status(500).send("An error occurred while processing the request.");
    }
});

app.get('/checkStatus', (req, res) => {
    const taskId = req.query.taskId;

    if (!taskId || !taskStatuses[taskId]) {
        return res.status(404).json({ error: "Task ID not found" });
    }

    const status = taskStatuses[taskId];
    res.json({ taskId, status });
});
