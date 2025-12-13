import classes from "./Dashboard.module.css";

const DashboardItemGroup = ({ title, children }) => {
    return (
        <div>
            <p className={ classes.title }>{ title }</p>
            { children }
        </div>
    );
}

export default DashboardItemGroup;