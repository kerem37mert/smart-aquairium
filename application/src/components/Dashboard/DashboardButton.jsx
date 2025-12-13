import classes from "./Dashboard.module.css";

const DashboardButton = ({ text, style, onClick }) => {
    return (
        <button className={ classes["dashboard-button"] } style={ style } onClick={ onClick }>
            { text }
        </button>
    );
}

export default DashboardButton;