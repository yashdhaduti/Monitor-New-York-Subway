import React, { useState } from 'react';
import axios from 'axios';


function MtaMonitor() {
    const [lineName, setLineName] = useState('');
    const [status, setStatus] = useState('');
    const [uptime, setUptime] = useState('');


    // shows status for given line name
    const checkStatus = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/status?line_name=${lineName.toUpperCase()}`);
            setStatus(response.data.status);
            setUptime("")
        } catch (error) {
            console.error(error);
            setStatus('error');
        }
      };

      // shows uptime for given line name
      const checkUptime = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/uptime?line_name=${lineName.toUpperCase()}`);
            setUptime(response.data.uptime.toFixed(4));
            setStatus("")
        } catch (error) {
            console.error(error);
            setUptime('error');
        }
      };
    
    return (
        <div>
        <h1>MTA Line Status</h1>
        <h4> Press the status or uptime button to see the status or uptime for a particular subway line</h4>
        <input
          type="text"
          placeholder="Enter line name"
          value={lineName}
          onChange={(e) => setLineName(e.target.value)}
        />
        <button onClick={checkStatus}>Check Status</button>
        <button onClick={checkUptime}>Check Uptime</button>
        {status !== '' && (
          <div>
            <h2>Line: {lineName.toUpperCase()}</h2>
            <p>Status: {status}</p>
          </div>
        )}
        {uptime !== '' && (
          <div>
            <h2>Line: {lineName.toUpperCase()}</h2>
            <p>Uptime: {uptime}</p>
          </div>
        )}
      </div>
    )
}




export default MtaMonitor;