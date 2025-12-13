import classes from "./Dashboard.module.css";

const DashBoardItem = ({ label, value }) => {
    return (
        <div className={ classes["dashboard-item"] }>
            <span className={ classes.label }>{ label }: </span>
            <span className={ classes.value }>{ value }</span>
        </div>
    );
}

export default DashBoardItem;