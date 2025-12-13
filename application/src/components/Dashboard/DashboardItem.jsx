import classes from "./Dashboard.module.css";

const DashBoardItem = ({ label, value, color="#000" }) => {
    return (
        <div className={ classes["dashboard-item"] }>
            <span className={ classes.label }>{ label }: </span>
            <span className={ classes.value }  style={{ color }} >{ value }</span>
        </div>
    );
}

export default DashBoardItem;