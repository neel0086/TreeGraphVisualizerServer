import express from 'express';
import serverless from 'serverless-http';
import cors from 'cors';
import bodyParser from 'body-parser';
const app = express();
import { router } from '../routes/route.js';
app.use(express.json({
    limit: '5mb',
    verify: (req, res, buf) => {
        // Capture the raw body as a string
        req.rawBody = buf.toString();
    },
}));

const allowedOrigins = ['https://quickfill.netlify.app', 'https://thequickfill.com','chrome-extension://gpiaempbpnopdfkohkkcocnlhbgllcjd','chrome-extension://ggmpijajgbagacnnnlghjjlneigfdbmh'];
app.use(cors({
    origin: (origin, callback) => {
        if (!origin || allowedOrigins.includes(origin)) {
            callback(null, true); // Allow if origin is in the allowed list or is undefined (e.g., Postman or server-to-server requests)
        } else {
            console.log("not allowed")
            callback(new Error('Not allowed by CORS'));
        }
    },
    methods: ['GET', 'POST'], // Specify allowed HTTP methods
    allowedHeaders: ['Content-Type', 'Authorization'], // Allow specific headers
}));

app.use(cors());
app.use(bodyParser.json({ extended: true }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/', router);

app.use('/.netlify/functions/api', router);
export const handler = serverless(app);
export default app
