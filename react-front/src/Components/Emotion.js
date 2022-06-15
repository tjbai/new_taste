import React from 'react'
import './Emotion.css'

const Emotion = ({emotion, value, max}) => {

    const baseStyle = {
        margin: '10px',
        height: '50px',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'inherit'
    }

    const emoStyle = (emotion, value) => {
        let c;
        switch (emotion) {
            case 'happy':
                c = '#f69c6d'
                break
            case 'surprise':
                c = '#ffcb69'
                break
            case 'neutral':
                c = '#997b66'
                break
            case 'disgust':
                c = '#87a70a'
                break
            case 'sad':
                c = '#219ebc'
                break
            case 'fear':
                c = '#c86bfa'
                break
            case 'angry':
                c = '#f94144'
                break
            default:
                break
        }

        // let w = 15*value
        // w = w < 75 ? 75 : w;
        // w = w > 400 ? 400 : w;
        let w = (value/max) * 400
        w = w < 60 ? 60 : w;

        return {
            ...baseStyle, 
            backgroundColor: c,
            width: `${w}px`,
            height: `${w/4}px`,
            fontSize: `${w/10}px`,
            borderRadius: `${w/10}px`,
            boxShadow: `${w/50}px ${w/50}px ${w/50}px black`
        }
    }

    return (
        <div 
            className='emotionIndicator' 
            style={emoStyle(emotion, value)}
        > 
            {emotion}: {Math.round(value * 100) / 100}%
        </div>
    )
}

export default Emotion