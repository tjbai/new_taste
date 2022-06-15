export const selectStyles = {
    control: (provided, state) => ({
        ...provided,
        background: '#fff',
        borderColor: '#9e9e9e',
        minHeight: '50px',
        borderRadius: '20px',
        padding: '5px',
        boxShadow: state.isFocused ? null : null,
      }),
  
      valueContainer: (provided, state) => ({
        ...provided,
      }),

      menuList: (provided, state) => ({
          ...provided,
          height: '200px'
      })
}
