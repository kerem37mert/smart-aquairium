import classes from "./Dashboard.module.css";

const Dashboard = ({  children }) => {
    return (
        <div className={ classes.dashboard }>
            { children }
        </div>
    );
}

export default Dashboard;