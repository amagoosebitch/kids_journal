import React from "react";
import './ActivityPage.css'
import {Header} from "../../components/header/Header";
import {useParams} from "react-router-dom";

type ActivityPageProps = {};

function ActivityPage({}: ActivityPageProps): JSX.Element {
    const { organization } = useParams();
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
