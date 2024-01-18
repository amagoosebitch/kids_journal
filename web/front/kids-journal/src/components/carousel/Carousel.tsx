import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Carousel.css";

import Slider from "react-slick";
import { useEffect, useState } from "react";

import { infoGroups, ApiRoute } from "../../const";
import { Link } from "react-router-dom";
import { ModalActive } from "../modalActive/ModalActive";

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
    subject_name: string;
    presentation_id: string;
    group_name: string;
    child_names: string[];
    date_day: string;
    description: string;
    is_for_child: boolean;
  },
];

export const lessonInfo: lessonInfoProps = [
  {
    schedule_id: "",
    subject_name: "",
    presentation_id: "",
    group_name: "",
    child_names: [""],
    date_day: "",
    description: "",
    is_for_child: false,
  },
];

export const Carousel = ({ organization, currentDate }: CarouselProps) => {
  const [carousels, setCarousels] = useState(infoGroups);

  const currentCarousel = carousels.filter((carousel) => {
    if (organization !== undefined)
      return carousel.organization
        .toLowerCase()
        .includes(organization.toLowerCase());
    return {};
  });

  const [groups, setGroups] = useState(groupInfo);
  const [lesson, setLesson] = useState(lessonInfo);
  const [allInfo, setAllInfo] = useState<
    { group: string; lessons: lessonInfoProps }[]
  >([]);

  useEffect(() => {
    fetch(`${ApiRoute}/organizations/${organization}/groups`, {
      method: "GET",
      headers: { Accept: "application/json" },
    })
      .then((response) => {
        if (response.status === 200 || response.status === 201) {
          return response;
        }
        throw new Error();
      })
      .then((response) => response.json())
      .then((data) => {
        setGroups(data);
      });
  }, []);

  useEffect(() => {
    setAllInfo([]);
  }, [currentDate]);

  const formatter = new Intl.DateTimeFormat("en-US", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });

  const formattedDate = formatter.format(currentDate);
  let dataArr = formattedDate.split("/");
  const resultData = dataArr[2] + "-" + dataArr[0] + "-" + dataArr[1];

  useEffect(() => {
    for (let i = 0; i < groups.length; i++) {
      if (groups[i].group_id !== "")
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
  }, [groups, currentDate]);

  let slidesToShowCurrent = 3;
  if (groups.length === 1) slidesToShowCurrent = 1;
  if (groups.length === 2) slidesToShowCurrent = 2;

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

  const [isOpenModal, setIsOpenModal] = useState(false);

  const [currentActivity, setCurrentActivity] = useState(lessonInfo);
  const [currentGroup, setCurrentGroup] = useState("");

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
                        <Link to={""} onClick={handleModalOpen}>
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
                                `Дети: ${lesson.child_names[0]} ${
                                  lesson.child_names.length > 1
                                    ? `и еще ${lesson.child_names.length - 1}`
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
