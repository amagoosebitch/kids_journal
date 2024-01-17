// export const ApiRoute = "https://d5de0lctsr23htkj7hlj.apigw.yandexcloud.net"
export const ApiRoute = "http://0.0.0.0:8080"
export const AppRoute = {
  WelcomeScreen: "/",
  Main: "/main",
  SignIn: "/login",
  SignUp: "/sign-up",
  Organizations: "/:organization",
  Groups: "/groups",
  Activity: "/activity",
  Subject: "/subject",
  Employees: "/employees",
  CreateActivity: "/createActivity",
  CreateGroups: "/createGroups",
  CreateEmployees: "/createEmployees",
  CreateSubject: "/createSubject",
  CreateOrganization: "/createOrganization",
  AddChild: "/addChild",
  Error: "/*",
};

export const LoginUrl = "https://d5de0lctsr23htkj7hlj.apigw.yandexcloud.net/login";
export const JwtKey = process.env.REACT_APP_JWT_SECRET_KEY

export enum AuthorizationStatus {
  Auth = "AUTH",
  NoAuth = "NO_AUTH",
  Unknown = "UNKNOWN",
}

export const infoOrganization = [
  {
    name: "Садик №1",
    id: "1",
  },
  {
    name: "Садик Вишенка",
    id: "2",
  },
];

export const infoGroups = [
  {
    organization: "Садик №1",
    carouselLabel: "Одуванчики",
    carouselAge: "0-3",
    carouselAction: [
      {
        carouselActionData: "2024-01-15T19:23",
        subject: "Что-то",
        carouselActionTitle: "Застегивание пуговиц",
        carouselActionCategory: true,
        children: [
          {
            name: "Болтов Егор",
          },
        ],
        description: "",
      },
      {
        carouselActionData: "2024-01-16T19:26",
        subject: "Что-то",
        carouselActionTitle: "Клеим марки",
        carouselActionCategory: false,
        children: [],
        description:
          "qwertyuikjbfbvjbdfvbgjfnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjk",
      },
      {
        carouselActionData: "2024-01-16T19:26",
        subject: "Что-то",
        carouselActionTitle: "Клеим марки",
        carouselActionCategory: false,
        children: [],
        description:
          "qwertyuikjbfbvjbdfvbgjfnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjk",
      },
      {
        carouselActionData: "2024-01-16T19:26",
        subject: "Что-то",
        carouselActionTitle: "Клеим марки",
        carouselActionCategory: false,
        children: [],
        description:
          "qwertyuikjbfbvjbdfvbgjfnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjk",
      },
      {
        carouselActionData: "2024-01-16T19:26",
        subject: "Что-то",
        carouselActionTitle: "Клеим марки",
        carouselActionCategory: false,
        children: [],
        description:
          "qwertyuikjbfbvjbdfvbgjfnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjk",
      },
      {
        carouselActionData: "2024-01-16T19:26",
        subject: "Что-то",
        carouselActionTitle: "Клеим марки",
        carouselActionCategory: false,
        children: [],
        description:
          "qwertyuikjbfbvjbdfvbgjfnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjk",
      },
      {
        carouselActionData: "2024-01-16T19:26",
        subject: "Что-то",
        carouselActionTitle: "Клеим марки",
        carouselActionCategory: false,
        children: [],
        description:
          "qwertyuikjbfbvjbdfvbgjfnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjk",
      },
      {
        carouselActionData: "2024-01-16T19:26",
        subject: "Что-то",
        carouselActionTitle: "Клеим марки",
        carouselActionCategory: false,
        children: [],
        description:
          "qwertyuikjbfbvjbdfvbgjfnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjk",
      },
    ],
    group_child: [
      {
        id: "",
        name: "Болтов Егор",
        birth_date: "2007-12-01",
        parents: [
          {
            id: "",
            name: "Болтова Инна Владимирована",
            phone_number: "+79998887766",
          },
        ],
      },
      {
        id: "",
        name: "Болтов Егорp",
        birth_date: "2007-12-01",
        parents: [
          {
            id: "",
            name: "Болтова Инна Владимирована",
            phone_number: "+79998887766",
          },
        ],
      },
    ],
  },
  {
    organization: "Садик №1",
    carouselLabel: "Ромашки",
    carouselAge: "3-6",
    carouselAction: [
      {
        carouselActionData: "2024-01-15T19:26",
        subject: "Что-то",
        carouselActionTitle: "Пить сок",
        carouselActionCategory: true,
        children: [
          {
            name: "Болтов Егор",
          },
          {
            name: "Болтов Егорр",
          },
        ],
        description: "",
      },
    ],
    group_child: [
      {
        id: "",
        name: "Болтов Егор",
        birth_date: "2007-12-01",
        parents: [
          {
            id: "",
            name: "Болтова Инна Владимирована",
            phone_number: "+79998887766",
          },
        ],
      },
    ],
  },
  {
    organization: "Садик №1",
    carouselLabel: "Васильки",
    carouselAge: "6-9",
    carouselAction: [
      {
        carouselActionData: "2024-01-15T19:26",
        subject: "Что-то",
        carouselActionTitle: "Застегивание пуговиц",
        carouselActionCategory: false,
        children: [],
        description: "",
      },
    ],
  },
  {
    organization: "Садик №1",
    carouselLabel: "Васильки",
    carouselAge: "6-9",
    carouselAction: [
      {
        carouselActionData: "2024-01-15T19:26",
        subject: "Что-то",
        carouselActionTitle: "Застегивание пуговиц",
        carouselActionCategory: true,
        children: [
          {
            name: "Болтов Егор",
          },
          {
            name: "Болтов Егорр",
          },
        ],
        description: "",
      },
    ],
    group_child: [
      {
        id: "",
        name: "Болтов Егор",
        birth_date: "2007-12-01",
        parents: [
          {
            id: "",
            name: "Болтова Инна Владимирована",
            phone_number: "+79998887766",
          },
        ],
        description: "",
      },
    ],
  },
];

export const infoEmployees = [
  {
    organization: "Садик №1",
    name: "Болтов Егор",
    role_id: "Администратор",
    phone_number: "+79998887766",
  },
  {
    organization: "Садик Вишенка",
    name: "Викулова Света",
    role_id: "Педагог",
    phone_number: "+79998887766",
  },
];

export const subjectInfo = [
  {
    organization: "Садик №1",
    name: "qwef",
    topic: [
      { name: "qwert", age: "3-6", description: "" },
      { name: "qwert11", age: "0-3", description: "" },
    ],
  },
  {
    organization: "Садик №1",
    name: "yqwef11",
    topic: [{ name: "qwert", age: "3-6", description: "" }],
  },
  {
    name: "qwef",
    topic: [
      { name: "qwert", age: "3-6", description: "" },
      { name: "qwert11", age: "0-3", description: "" },
    ],
  },
];
