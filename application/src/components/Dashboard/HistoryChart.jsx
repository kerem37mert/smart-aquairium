import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';

const HistoryChart = ({ data }) => {
    if (!data || data.length === 0) return null;

    return (
        <div style={{
            backgroundColor: 'white',
            padding: '20px',
            marginTop: '20px',
            border: "2px solid gray"
        }}>
            <h3 style={{ color: '#333', marginBottom: '20px' }}>Canlı Su Değerleri</h3>
            <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                    <LineChart
                        data={data}
                        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" />
                        <YAxis yAxisId="left" />
                        <YAxis yAxisId="right" orientation="right" />
                        <Tooltip />
                        <Legend />
                        {/* isAnimationActive={false} prevents the line from "growing" from 0 on every update, creating a smooth scrolling effect */}
                        <Line yAxisId="left" type="monotone" dataKey="ph" stroke="#8884d8" name="pH" dot={false} isAnimationActive={false} strokeWidth={2} />
                        <Line yAxisId="right" type="monotone" dataKey="temperature" stroke="#ff4d4d" name="Sıcaklık" dot={false} isAnimationActive={false} strokeWidth={2} />
                        <Line yAxisId="left" type="monotone" dataKey="ammonia" stroke="#82ca9d" name="Amonyak" dot={false} isAnimationActive={false} strokeWidth={2} />
                        <Line yAxisId="left" type="monotone" dataKey="nitrite" stroke="#ffc658" name="Nitrit" dot={false} isAnimationActive={false} strokeWidth={2} />
                        <Line yAxisId="left" type="monotone" dataKey="nitrate" stroke="#ff7300" name="Nitrat" dot={false} isAnimationActive={false} strokeWidth={2} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default HistoryChart;
