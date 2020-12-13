import React from 'react';
import '../App.css'

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Statistic } from 'antd';


import data from '../db.json';

const Statistics = () => {
    const [parsingTime, setParsingTime] = React.useState(); // [{match_number, time}]
    const [averageParseTime, setAverageParseTime] = React.useState(); // Integer
    const [checked, setChecked] = React.useState();
    const [correct, setCorrect] = React.useState();
    const [winrate, setWinrate] = React.useState();

    const average = arr => (arr.reduce( ( p, c ) => p + c, 0 ) / arr.length).toFixed(2)

    const processData = () => {
        let parsing_time = []
        let checking_time = []
        let checked = 0;
        let correct_predictions = 0
        Object.keys(data).forEach((matchID, i) => {
            let match = data[matchID];
            if( data[matchID].parsing_time ) parsing_time.push({match_number: i+1, time: data[matchID].parsing_time})
            if( data[matchID].prediction_correct ) correct_predictions++;
            if( typeof match.prediction_correct !== "undefined" ) checked++;
        })

        setParsingTime(parsing_time);
        setAverageParseTime(average(parsing_time.map(item => item.time)))
        setChecked(checked);
        setCorrect(correct_predictions);
        setWinrate((correct_predictions/checked * 100).toFixed(2))
    }

    React.useEffect(() => {
        processData();
    }, [])

    return (
        <div className="page">
            <span className="header">Faugur Statistics</span>

            <Statistic className="stats" title="Total matches" value={Object.keys(data).length} />
            <Statistic className="stats" title="Matches checked" value={checked} />
            <Statistic className="stats" title="Predictions correct" value={correct} />
            <Statistic className="stats" title="Prediction Rate" value={winrate} />

            <div className="chart">
                <Statistic className="stats" title="Average parsing time" value={averageParseTime} />
                <ResponsiveContainer width="80%" height={500}>
                    <LineChart
                        data={parsingTime}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="match_number" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="time" stroke="#82ca9d" />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

export default Statistics;