import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import { router } from '../routes/route.js';

const app = express();

// CORS Setup
const allowedOrigins = [
  'https://quickfill.netlify.app',
  'https://thequickfill.com',
  'chrome-extension://gpiaempbpnopdfkohkkcocnlhbgllcjd',
  'chrome-extension://ggmpijajgbagacnnnlghjjlneigfdbmh',
];
app.use(
  cors({
    origin: (origin, callback) => {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error('Not allowed by CORS'));
      }
    },
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type', 'Authorization'],
  })
);

// Middleware
app.use(express.json({ limit: '5mb' }));
app.use(bodyParser.json({ extended: true }));
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
app.use('/', router);

// Start server (required for Render)
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
