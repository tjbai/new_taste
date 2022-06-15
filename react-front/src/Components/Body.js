import React, { 
    useRef, 
    useCallback, 
    useState,
    useEffect
} from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import * as ReactBootStrap from 'react-bootstrap'
import * as tf from '@tensorflow/tfjs';
import Select from 'react-select';
import * as facemesh from '@tensorflow-models/facemesh';

import './Body.css';
import ResultsDashboard from './ResultsDashboard';
import { genres } from '../helper/constants.js'
import { drawMesh } from '../helper/mesh.js';
import { selectStyles } from '../helper/selectStyles'

const OPTIONS = genres.map(genre => ({
    label: genre,
    value: genre
}))

const VIDEO_CONST = {
    height: 500,
    width: 500,
    facingMode: 'user'
};
const IMG_HEADER = 'data:image/jpeg;base64,'
const SONG_COUNT = 3;
const WIDTH = 500;
const HEIGHT = 500;


const Body = () => {
    const wcRef = useRef(null); // Webcam ref
    const canvasRef = useRef(null); // Canvas ref
    
    const [loading, setLoading] = useState(false); 
    const [genreFilter, setGenreFilter] = useState([]); 

    // For the results dashboard
    const [detectState, setDetectState] = useState({
        faceCount: 0,
        faceImg: null,
        emotions: ['test'],
        songs:  [...Array(3)].map(e => Array(6))
    });

    // Load facemesh
    const runFacemesh = async () => {
        const net = await facemesh.load({
            inputResolution:{width:WIDTH, height:HEIGHT}, 
            scale:0.8
        }); 
        setInterval(() => {
            detect(net)
        }, 100);
    }

    // Landmark detection function
    const detect = async (net) => {
         if (
            typeof(wcRef.current) !== 'undefined' && 
            wcRef.current !== null && 
            wcRef.current.video.readyState === 4
        ) {
            const video = wcRef.current.video;

            wcRef.current.video.width = WIDTH;
            wcRef.current.video.height = HEIGHT;
            canvasRef.current.width = WIDTH;
            canvasRef.current.height = HEIGHT;

            const face = await net.estimateFaces(video);
            const context = canvasRef.current.getContext('2d')
            drawMesh(face, context, WIDTH);
        }   
    }

    // Press button -> post screenshot to api -> manage response
    const capture = useCallback(async () => {
        const imageSrc = wcRef.current.getScreenshot();
        setLoading(true);
        try {
            const update = await axios
                .post('http://127.0.0.1:5000/api', {
                    img: imageSrc,
                    songCount: SONG_COUNT,
                    genreFilter: genreFilter
                })
                .then(res => {
                    setDetectState({
                        faceCount: res.data.count,
                        faceImg: IMG_HEADER+res.data.img,
                        emotions: res.data.emotions,
                        songs: res.data.songs
                    })
                }) 
            setLoading(false);
        } catch (e) {
            console.log(e);
        }
    }, [wcRef, genreFilter]); 

    useEffect(() => {
        runFacemesh();
    }, []) 

    return (
        <section className="body">

            <div id='camBackground' >
                <Webcam 
                    id='webcam'
                    ref={wcRef} 
                    audio={false} 
                    width={WIDTH} 
                    height={HEIGHT} 
                    screenshotFormat='image/jpeg' 
                    mirrored={true}
                    videoConstraints={VIDEO_CONST} 
                />

                <canvas
                    id='canvas'
                    width={WIDTH}
                    height={HEIGHT}
                    ref={canvasRef}
                />
            </div>

            <Select 
                id='genreFilter'
                placeholder={'Give me anything!'}
                options={OPTIONS}
                isMulti={true}
                onChange={(e) => {
                    setGenreFilter(e)
                }}
                styles={selectStyles}
            />

            <button 
                id='detectButton'
                onClick={capture}>DETECT
            </button>

            {loading 
            ? (<ReactBootStrap.Spinner animation='border' />) 
            : (<ResultsDashboard state={detectState} />) }

        </section>
    )
}

export default Body