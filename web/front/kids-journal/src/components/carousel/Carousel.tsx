import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Carousel.css";

import Slider from "react-slick";
import React, { useEffect, useState } from "react";

import { ApiRoute, infoGroups, testOrganization } from "../../const";
import { Link } from "react-router-dom";
import { ModalActive } from "../modalActive/ModalActive";
import {useAppDispatch, useAppSelector} from "../../hooks/useAppDispatch";
import { fetchGroupsAction } from "../../store/api-actions";
import { store } from "../../store";
import {getAllData} from "../../features/groupsSlice";
import {LoaderScreen} from "../../pages/loading-screen/LoaderScreen";

export type CarouselProps = {
  organization: string | undefined;
  currentDate: Date;
};

export const groupInfo = [
  {
    group_id: "",
    organization_id: "",
    name: "",
    age_range: "",
  },
];

type lessonInfoProps = [
  {
    schedule_id: string;
    presentation_id: string;
    child_ids: string[];
    date_day: string;
    is_for_child: boolean;
  },
];

export const lessonInfo: lessonInfoProps = [
  {
    schedule_id: "",
    presentation_id: "",
    child_ids: [""],
    date_day: "",
    is_for_child: false,
  },
];

export const Carousel = ({ organization, currentDate }: CarouselProps) => {
  const [carousels, setCarousels] = useState(infoGroups);
  const [isOpenModal, setIsOpenModal] = useState(false);

  const [currentActivity, setCurrentActivity] = useState(lessonInfo);
  const [currentGroup, setCurrentGroup] = useState("");
  const [currentTeacher, setCurrentTeacher] = useState("");

  const currentCarousel = carousels.filter((carousel) => {
    if (organization !== undefined)
      return carousel.organization
        .toLowerCase()
        .includes(organization.toLowerCase());
    return {};
  });

  const [allInfo, setAllInfo] = useState<
    { group: string; lessons: lessonInfoProps }[]
  >([]);

  const dispatch = useAppDispatch();
  const data = useAppSelector((state) => {
    return state.groups;
  });

  const groups = data.groups;

  useEffect(() => {
    dispatch(getAllData())
  }, [])

  useEffect(() => {
    setAllInfo([]);
  }, [currentDate]);

  useEffect(() => {
    for (let i = 0; i < groups.length; i++) {
      if (groups[i].group_id !== "") {
        console.log(groups[i].group_id);
        fetch(
            `${ApiRoute}/lessons/${groups[i].group_id}?date_day=${resultData}`,
            {
              method: "GET",
              headers: { Accept: "application/json" },
            },
        )
            .then((response) => {
              if (response.status === 200 || response.status === 201) {
                return response;
              }
              throw new Error();
            })
            .then((response) => response.json())
            .then((data) => {
              if (data.length !== 0)
                setAllInfo((allInfo) => [
                  ...allInfo,
                  { group: groups[i].group_id, lessons: data },
                ]);
            });
      }
    }
  }, [groups, currentDate]);


  // const [groups, setGroups] = useState(groupInfo);
  // useEffect(() => {
  //   fetch(`${ApiRoute}/organizations/${testOrganization}/groups`, {
  //     method: "GET",
  //     headers: { Accept: "application/json" },
  //   })
  //     .then((response) => {
  //       if (response.status === 200 || response.status === 201) {
  //         return response;
  //       }
  //       throw new Error();
  //     })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setGroups(data);
  //     });
  // }, []);


  const formatter = new Intl.DateTimeFormat("en-US", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });

  const formattedDate = formatter.format(currentDate);
  let dataArr = formattedDate.split("/");
  const resultData = dataArr[2] + "-" + dataArr[0] + "-" + dataArr[1];

  let slidesToShowCurrent = 3;
  if (groups.length === 1) slidesToShowCurrent = 1;
  else if (groups.length === 2) slidesToShowCurrent = 2;

  let settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: slidesToShowCurrent,
    slidesToScroll: 3,
    initialSlide: 0,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: slidesToShowCurrent === 1 ? 1 : slidesToShowCurrent - 1,
          slidesToScroll:
            slidesToShowCurrent === 1 ? 1 : slidesToShowCurrent - 1,
          infinite: true,
          dots: true,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          initialSlide: 1,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };

  const formatData = currentDate.toLocaleDateString();

  const doDo = (action: lessonInfoProps, group: string) => {
    setCurrentActivity(action);
    setCurrentGroup(group);
  };

  const handleModalOpen = () => {
    setIsOpenModal(true);
  };

  const handleModalClose = () => {
    setIsOpenModal(false);
  };

  return (
    <>
      <div className="carousel">
        <Slider {...settings}>
          {groups.map((group) => (
            <div className="carousel_box">
              <div className="carousel_box-title">
                <div className="carousel_box-name">Группа {group.name}</div>
                <div className="carousel_box-age">{group.age_range}</div>
              </div>
              {allInfo.filter((el) => {
                return el.group === group.name;
              }).length !== 0 && (
                <div className="carousel_box-content">
                  {allInfo
                    .filter((el) => {
                      return el.group === group.name;
                    })
                    .map((action) =>
                      action.lessons.map((lesson) => (
                        <Link
                          className="carousel_box-container"
                          to={""}
                          onClick={handleModalOpen}
                        >
                          <div
                            onClick={() => doDo([lesson], group.name)}
                            className={`carousel_box-action ${
                              lesson.is_for_child ? "isOrange" : "isGreen"
                            }`}
                          >
                            <div className="carousel_action-info">
                              <div className="carousel_action-topic">
                                {lesson.presentation_id}
                              </div>
                              <div className="carousel_action-time">
                                {lesson.date_day.split("T")[1].slice(0, 5)}
                              </div>
                            </div>
                            <div className="carousel_action-children">
                              {lesson.is_for_child &&
                                `Дети: ${lesson.child_ids[0]} ${
                                  lesson.child_ids.length > 1
                                    ? `и еще ${lesson.child_ids.length - 1}`
                                    : ""
                                }`}
                            </div>
                          </div>
                        </Link>
                      )),
                    )}
                </div>
              )}
            </div>
          ))}
        </Slider>
      </div>
      <ModalActive
        isOpen={isOpenModal}
        onCloseModal={handleModalClose}
        currentActivity={currentActivity}
        currentGroup={currentGroup}
      />
    </>
  );
};
