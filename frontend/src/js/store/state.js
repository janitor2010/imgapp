export default {
    Comments: {
      Items: [
          {
            id: 1,
            name: 11,
            phone: 222
          },
          {
            id: 2,
            name: 222,
            phone: 44444
          },
          {
            id: 3,
            name: 55,
            phone: 8888
          },
          {
            id: 4,
            name: 55,
            phone: 8888
          },
          {
            id: 5,
            name: 55,
            parentId: 1,
            phone: 8888
          },
          {
            id: 6,
            name: 55,
            parentId: 2,
            phone: 8888
          },
          {
            id: 7,
            name: 55,
            parentId: 2,
            phone: 8888
          },
        ],
      Model: [
        {
          type: 'vInput',
          name: 'name'
        },
        {
          type: 'vInput',
          name: 'phone'
        },
        {
          type: 'hidden',
          name: 'id'
        },
        {
          type: 'hidden',
          name: 'parentId'
        }
      ],
      EditedItems: []
    }
}
