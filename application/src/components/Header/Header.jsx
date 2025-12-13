import classes from "./Header.module.css";

const Header = ({ title }) => {
    return (
        <div className={ classes.header }>
            <h2 className={ classes.title }>{ title }</h2>
        </div>
    );
}

export default Header;