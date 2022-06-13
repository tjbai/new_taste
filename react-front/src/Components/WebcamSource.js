import React, { useRef, useCallback, useState } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import * as ReactBootStrap from 'react-bootstrap'

import { Results } from './Results'

let IMG_HEADER = 'data:image/jpeg;base64,'

export const WebcamSource = () => {
    const wcRef = useRef(null);
    const [detectState, setDetectState] = useState({
        faceCount: 0,
        faceImg: null,
        emotions: ['test'],
        songs:  [...Array(3)].map(e => Array(6))
    });
    const [loading, setLoading] = useState(false);
    const [songCount, setSongCount] = useState(3);

    const videoConstraints = {
        width: 300,
        height: 300,
        facingMode: 'user'
    };

    const capture = useCallback(async () => {
        const imageSrc = wcRef.current.getScreenshot();
        setLoading(true);
        try {
            const update = await axios
                .post('http://127.0.0.1:5000/api', {
                    img: imageSrc,
                    songCount: songCount
                })
                .then(res => {
                    setDetectState({
                        faceCount: res.data.count,
                        faceImg: IMG_HEADER+res.data.img,
                        emotions: res.data.emotions,
                        songs: res.data.songs
                    })

                    console.log(res.data)
                }) 
            setLoading(false);
        } catch (e) {
            console.log(e);
        }
    }, [wcRef]);

    return (
        <div>
            <Webcam 
                ref={wcRef} 
                audio={false} 
                height={300} 
                screenshotFormat='image/jpeg' 
                width={350} 
                mirrored={true}
                videoConstraints={videoConstraints} />
            <button 
                onClick={capture}>DETECT</button>

            {loading 
                ? (<ReactBootStrap.Spinner animation='border' />) 
                : (<Results state={detectState} />) }
        </div>
    )
}