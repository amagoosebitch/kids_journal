import React from "react";
import './ActivityPage.css'
import {Header} from "../../components/header/Header";

type ActivityPageProps = {};

function ActivityPage({}: ActivityPageProps): JSX.Element {
    return (
        <div>
            <Header/>
            <div className='activity_container'>
                <div className='activity_item'>Наблюдения</div>
                <div className='activity_item'>Упражнения</div>
                <div className='activity_item'>Диагностика</div>
            </div>
        </div>
    );
}

export default ActivityPage;
