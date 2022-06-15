import React from 'react';
import Emotion from './Emotion'

const EmotionDashboard = (emotionVals) => {
    let res = [
        'angry', 
        'disgust', 
        'fear', 
        'happy',
        'neutral', 
        'sad', 
        'surprise'
    ];

    let dict = emotionVals['emotionvals']
    res.sort(function(x, y) {
        if (dict[x] < dict[y]) {
            return 1;
        }
        return -1;
    });

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'flex-start',
            margin: '50px'
        }}>
            {res.map((e) => 
                <Emotion 
                    key={e} 
                    emotion={e} 
                    value={dict[e]}
                    max={dict[res[0]]}
                />
            )}
        </div>
    );
};

export default EmotionDashboard;