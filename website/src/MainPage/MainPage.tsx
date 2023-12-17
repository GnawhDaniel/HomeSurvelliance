import { useState } from "react";
import styles from "./MainPage.module.css";
// import dotenv from 'dotenv';

// dotenv.config({ path: '../.env' });

const WS_URL = import.meta.env.VITE_SERVER_URL;
const ws = new WebSocket(WS_URL);


let urlObject = "";

const MainPage = () => {
    
    const [imgUrl, setImgUrl] = useState("/nocamera.png");

    ws.onopen = () => {
        ws.send('web')
    }
    ws.onmessage = (message) => {
        const arrayBuffer = message.data;
        if (urlObject) {
            URL.revokeObjectURL(urlObject);
        }
        urlObject = URL.createObjectURL(new Blob([arrayBuffer]));
        setImgUrl(urlObject);
    };
    ws.onerror = (message) => {
        console.log(message);
    };

    const [email, setEmail] = useState('');
    const [isValidEmail, setIsValidEmail] = useState(false);

    const validateEmail = (email:string) => {
        const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return re.test(String(email).toLowerCase());
    };

    const handleEmailChange = (newEmail: string) => {
        setEmail(newEmail);
        setIsValidEmail(validateEmail(newEmail));
    };

    const handleSubmit = (event: any) => {
        event.preventDefault();
        // Handle the form submission here (e.g., send data to a server)
        if (email != "") {
            try {
                ws.send(email);
            }
            catch(error){}
            console.log(email); 
            setEmail("");
            setIsValidEmail(false);
        }

    };

    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: '#A7C7E7' }}>
                <span className="navbar-brand ms-3">CS 147 Project - Home Security</span>
            </nav>
            <div className="d-flex justify-content-center m-5">
                <img className={styles.image} src={imgUrl}></img>
            </div>

            <div className="m-5">
                <h1 className="mb-2">Notify Me Please</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="exampleInputEmail1" className='mb-1'>Email address</label>
                        <input onChange={e=>handleEmailChange(e.target.value)} value={email} type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email"/>
                        <small id="emailHelp" className="form-text text-muted">We will mail detections to this email address.</small>
                    </div>
                    <button type="submit" className="btn btn-primary" disabled={!isValidEmail}>Submit</button>
                </form>
            </div>
        </>
    );
};

export default MainPage;