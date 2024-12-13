const express = require('express');
const mysql = require('mysql');

const app = express();
const port = 3001;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
    next();
});

var dbConfig = {
    host: 'localhost',
    user: 'nitsilchar',
    password: 'TAR0HA=#UMF_'
};

var connection = mysql.createConnection(dbConfig);

connection.connect(err => {
    if (err) {
        console.error('Database connection failed:', err);
        return;
    }
    else {console.log('Database connected');}
});

connection.query("CREATE DATABASE IF NOT EXISTS `lipsync`", function (err, result) {
    if (err) throw err;
    else console.log(result)
})

dbConfig = {
    host: 'localhost',
    user: 'nitsilchar',
    password: 'TAR0HA=#UMF_',
    database: 'lipsync'
};

connection = mysql.createConnection(dbConfig);

connection.connect(err => {
    if (err) {
        console.error('Database connection failed:', err);
        return;
    }
    else {console.log('Database connected');}
});

connection.query("CREATE TABLE IF NOT EXISTS `lipsync`.`userregdetails` (`uid` INT NOT NULL AUTO_INCREMENT , `u_fname` TEXT NOT NULL , `u_lname` TEXT NOT NULL , `u_mail` VARCHAR(90) NOT NULL , `u_pass` VARCHAR(16) NOT NULL , `u_reg_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`uid`))", function (err, result) {
    if (err) throw err;
    console.log(result)
})

connection.query("SELECT * FROM `userregdetails`", function (err, result) {
    if (err) throw err;
    app.get("/api", (req, res) => {
        res.json(result);
    });
    console.log(result)
})

app.post('/api/users', (req, res) => {
    const { u_fname, u_lname, u_mail, u_pass } = req.body;
    const query = 'INSERT INTO `lipsync`.`userregdetails` (u_fname, u_lname, u_mail, u_pass) VALUES (?, ?, ?, ?)';

    connection.query("SELECT * FROM `userregdetails`", function (err, result) {
        if (err) throw err;
        app.get("/api", (req, res) => {
            res.json(result);
        });
        console.log(result)
    })

    connection.query(query, [u_fname, u_lname, u_mail, u_pass], (err, result) => {
        if (err) {
            console.error('Query failed:', err);
            return res.status(500).send('Query failed');
        }
        app.get("/api/" + u_mail, (req, res) => {
            res.json(result)
        })
        res.send('Data inserted successfully');
    });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
