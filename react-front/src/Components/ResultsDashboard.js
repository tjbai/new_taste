import React from 'react'

import './ResultsDashboard.css'
import EmotionDashboard from './EmotionDashboard'
import SongDashboard from './SongDashboard'

export const ResultsDashboard = (state) => {
    return (
        <div id='dashboard'>
            <img id='resultImg' src={state.state.faceImg} />
            <EmotionDashboard emotionvals={state.state.emotions} />
            <SongDashboard songs={state.state.songs} />
        </div>
    )
}

export default ResultsDashboard;