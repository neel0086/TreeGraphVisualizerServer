import express from 'express';
import { codeRunner } from '../controller/CodeController.js';



const router = express.Router();

router.get('/', (req, res) => {
    res.send('App is running..');
});

//POST REQUEST
router.post("/codeRunner", codeRunner)


//GET REQUEST

//PUT REQUEST
export { router };
